from __future__ import annotations
from collections import Counter

import logging
import operator
import warnings
from functools import reduce
from typing import Any, Optional, Sequence

from django import forms
import django.core.exceptions
from django.contrib import admin
from django.http import HttpRequest
from ordered_model.admin import OrderedInlineModelAdminMixin, OrderedModelAdmin, OrderedTabularInline

from django.db.models import JSONField

from formkit_ninja import formkit_schema, models

logger = logging.getLogger(__name__)


# Define fields in JSON with a tuple of fields
# The key of the dict provided is a JSON field on the model
JsonFieldDefn = dict[str, tuple[str | tuple[str, str], ...]]


class ItemAdmin(OrderedModelAdmin):
    list_display = ("name", "move_up_down_links")


class JsonDecoratedFormBase(forms.ModelForm):
    """
    Adds additional fields to the admin where a model has a JSON field
    and some appropriate (tbc?) field parameters
    """

    # extra = forms.CharField(label="Extra", max_length=128, required=False)
    # hello_world = forms.CharField(widget=forms.NumberInput, required=False)

    # key is the name of a `models.JSONField` on the model
    # value is a list of fields to get/set in that JSON field
    _json_fields: JsonFieldDefn = {"my_json_field": ("formkit", "description", "name", "key", "html_id")}

    def get_json_fields(self) -> JsonFieldDefn:
        """
        Custom which json fields will be included in the return
        """
        return self._json_fields

    def _field_check(self):
        """
        Check that JSON fields specified are json fields on the model
        do not clash with model fields
        """

        def check_json_fields_exist():
            """
            Check that JSON fields specified are json fields on the model
            """
            for field in self.get_json_fields().keys():
                try:
                    model_field = self.Meta.model._meta.get_field(field)
                    if not isinstance(model_field, JSONField):
                        raise KeyError(f"Expected a JSONField named {field} on the model")
                except django.core.exceptions.FieldDoesNotExist as E:
                    raise KeyError(f"Expected a JSONField named {field} on the model") from E

        def check_no_duplicates():
            """
            Checks that the `_json_fields` specified do not clash with fields 
            on the model
            """
            fields_in_model = Counter(self.Meta.fields)

            # These are all the fields we've "JSON"ified
            for json_keys in self.get_json_fields().values():
                fields_in_model.update((k for k in json_keys if isinstance(k, str)))
                fields_in_model.update((k[0] for k in json_keys if not isinstance(k, str)))

            # Duplicate fields raise an exception
            duplicates = list(((k, v) for k, v in fields_in_model.items() if v > 1))
            if duplicates:
                raise KeyError(f"Some fields were duplicated: {','.join(duplicates)}")
            
        check_json_fields_exist()
        check_no_duplicates()

    def _set_json_fields(self, instance):
        """
        Assign JSON field content to Form fields
        """
        for field, keys in self.get_json_fields().items():
            # Extract the dict of JSON values from the model instance if supplied
            values = getattr(instance, field, {}) or {}  # Don't allow none:
            # field_name is the property on the ModelForm to use.
            # This allows "aliasing" so that fields on the model / JSON are not shadowed.
            for key in keys:
                if isinstance(key, str):
                    form_field = key
                    json_field = key
                else:
                    form_field, json_field = key
                # The value, extracted from the JSON value in the database
                field_value = values.get(json_field, None)
                # The initial value of the admin form is set to the value of the JSON attrib
                self.fields.get(form_field).initial = field_value

    def __init__(self, *args, **kwargs):
        """
        When the form is initialized, additional "Fields"
        can be populated from a JSON data field.
        """
        super().__init__(*args, **kwargs)
        if instance := kwargs['instance']:
            self._set_json_fields(instance)

    def save(self, commit=True):
        """
        Updates the JSON field(s) from the fields specified in the `_json_fields` dict
        """

        for field, keys in self.get_json_fields().items():
            # Populate a JSON field in a model named "form"
            # from a set of standard form elements
            data = {}
            for key in keys:
                if isinstance(key, str):
                    form_field = key
                    json_field = key
                else:
                    form_field, json_field = key
                if cleaned_data := self.cleaned_data[json_field]:
                    data[form_field] = cleaned_data
        setattr(self.instance, field, data)
        return super().save(commit=commit)


class NewFormKitForm(forms.ModelForm):
    class Meta:
        model = models.FormKitSchemaNode
        fields = ("label", "node_type", "description")


class OptionForm(forms.ModelForm):
    class Meta:
        model = models.Option
        exclude = ()


class FormComponentsForm(forms.ModelForm):
    class Meta:
        model = models.FormComponents
        exclude = ()


class FormKitSchemaNodeOptionsInline(OrderedTabularInline):
    model = models.Option
    form = OptionForm
    fields = ("value",)
    readonly_fields = (
        "order",
        "move_up_down_links",
    )
    ordering = ("order",)
    extra = 0


class FormKitSchemaComponentInline(OrderedTabularInline):
    model = models.FormComponents
    readonly_fields = (
        "node",
        "created_by",
        "updated_by",
        "order",
        "move_up_down_links",
    )
    ordering = ("order",)
    extra = 0


class FormKitNodeGroupForm(JsonDecoratedFormBase):
    class Meta:
        model = models.FormKitSchemaNode
        fields = ("label", "description", "additional_props")

    _json_fields = {
        "node": (
            "formkit",
            "if_condition",
        )
    }

    formkit = forms.ChoiceField(required=False, choices=models.FormKitSchemaNode.FORMKIT_CHOICES, disabled=True)
    if_condition = forms.CharField(
        widget=forms.TextInput,
        required=False,
    )


class FormKitNodeForm(JsonDecoratedFormBase):
    """
    This is the most common component type: the 'FormKit' schema node
    """

    class Meta:
        model = models.FormKitSchemaNode
        fields = ("label", "description", "additional_props")

    # The `_json_fields["node"]` item affects the admin form,
    # adding the fields included in the `FormKitSchemaProps.__fields__.items` dict
    _json_fields = {
        "node": (
            "formkit",
            ("node_description", "description"),  # This tuple escapes a conflict with model field
            "name",
            "key",
            "html_id",
            "if_condition",
            "options",
            ("node_label", "label"),
            "placeholder",
            "help",
            # Validation of fields
            "validation",
            "validationLabel",
            "validationVisibility",
            "validationMessages",
            "prefixIcon",
            # Numeric forms
            "min",
            "max",
            "step",
        )
    }

    formkit = forms.ChoiceField(required=False, choices=models.FormKitSchemaNode.FORMKIT_CHOICES)
    name = forms.CharField(required=False)
    if_condition = forms.CharField(widget=forms.TextInput, required=False)
    key = forms.CharField(required=False)
    label = forms.CharField(required=False)
    node_label = forms.CharField(required=False)
    node_description = forms.CharField(required=False)
    placeholder = forms.CharField(required=False)
    help = forms.CharField(required=False)
    html_id = forms.CharField(
        required=False, help_text="Use this ID if adding conditions to other fields (hint: $get(my_field).value === 8)"
    )
    options = forms.CharField(
        required=False, help_text="Use this if adding Options using a JS function (hint: $get(my_field).value )"
    )
    validation = forms.CharField(required=False)
    validationLabel = forms.CharField(required=False)
    validationVisibility = forms.CharField(required=False)
    validationMessages = forms.JSONField(required=False)
    validationRules = forms.CharField(
        required=False, help_text="A function for validation passed into the schema: a key on `formSchemaData`"
    )
    prefixIcon = forms.CharField(required=False)

    # NumberNode props

    max = forms.IntegerField(required=False)
    min = forms.IntegerField(required=False)
    step = forms.IntegerField(required=False)

    def get_fields(self, request, obj: models.FormKitSchemaNode):
        """
        Customise the returned fields based on the type
        of formkit node
        """
        return super().get_fields(request, obj)


class FormKitNodeRepeaterForm(FormKitNodeForm):
    def get_json_fields(self) -> JsonFieldDefn:
        return {
            "node": (
                *(super()._json_fields["node"]),
                "addLabel",
                "upControl",
                "downControl",
                "itemsClass",
                "itemClass",
            )
        }

    addLabel = forms.CharField(required=False)
    upControl = forms.BooleanField(required=False)
    downControl = forms.BooleanField(required=False)
    itemsClass = forms.CharField(required=False)
    itemClass = forms.CharField(required=False)
    max = forms.IntegerField(required=False)
    min = forms.IntegerField(required=False)


class FormKitTextNode(JsonDecoratedFormBase):
    class Meta:
        model = models.FormKitSchemaNode
        fields = (
            "label",
            "description",
        )

    _json_fields = {"node": ("content",)}
    content = forms.CharField(
        widget=forms.TextInput,
        required=True,
    )


class FormKitElementForm(JsonDecoratedFormBase):
    class Meta:
        model = models.FormKitSchemaNode
        fields = ("label", "description", "text_content")

    _skip_translations = {"label", "placeholder"}
    _json_fields = {"node": ("el", "name", "if_condition", "classes")}

    el = forms.ChoiceField(required=False, choices=models.FormKitSchemaNode.ELEMENT_TYPE_CHOICES)
    name = forms.CharField(
        required=False,
    )
    classes = forms.CharField(
        required=False,
    )
    if_condition = forms.CharField(
        widget=forms.TextInput,
        required=False,
    )


class FormKitConditionForm(JsonDecoratedFormBase):
    class Meta:
        model = models.FormKitSchemaNode
        # fields = '__all__'
        fields = (
            "label",
            "description",
        )

    _json_fields = {"node": ("if_condition", "then_condition", "else_condition")}

    if_condition = forms.CharField(
        widget=forms.TextInput,
        required=False,
    )
    then_condition = forms.CharField(
        max_length=256,
        required=False,
    )
    else_condition = forms.CharField(
        max_length=256,
        required=False,
    )


class FormKitComponentForm(JsonDecoratedFormBase):
    class Meta:
        model = models.FormKitSchemaNode
        fields = (
            "label",
            "description",
        )

    _json_fields = {"node": ("if_condition", "then_condition", "else_condition")}


class MembershipInline(OrderedTabularInline):
    model = models.Membership
    fk_name = "group"
    extra = 0
    readonly_fields = (
        "order",
        "move_up_down_links",
    )
    ordering = ("order",)


class MembershipComponentInline(admin.StackedInline):
    model = models.Membership
    fk_name = "member"
    extra = 0


class NodeChildrenInline(OrderedTabularInline):
    """
    Nested HTML elements
    """

    model = models.NodeChildren
    fields = ("child", "order", "move_up_down_links")
    readonly_fields = (
        "order",
        "move_up_down_links",
    )
    ordering = ("order",)
    fk_name = "parent"
    extra = 0


class FormKitSchemaForm(forms.ModelForm):
    class Meta:
        model = models.FormKitSchema
        exclude = ("name",)


@admin.register(models.FormKitSchemaNode)
class FormKitSchemaNodeAdmin(OrderedInlineModelAdminMixin, admin.ModelAdmin):
    list_display = ("label", "id", "node_type")

    def get_inlines(self, request, obj: models.FormKitSchemaNode | None):
        if not obj:
            return []

        formkit_node_type = (obj.node or {}).get("formkit", None)

        if formkit_node_type == "group":
            return [
                NodeChildrenInline,
            ]
        elif formkit_node_type in {"radio", "select", "dropdown"}:
            return [
                MembershipComponentInline,
                FormKitSchemaNodeOptionsInline,
            ]
        elif formkit_node_type:
            return [
                MembershipComponentInline,
            ]

        if obj.node_type == "$el":
            return [
                NodeChildrenInline,
            ]

        else:
            return []

    # # Note that although overridden these are necessary
    # inlines = [NodeChildrenInline]
    inlines = [FormKitSchemaNodeOptionsInline, NodeChildrenInline, MembershipInline]

    def get_fieldsets(
        self, request: HttpRequest, obj: models.FormKitSchemaNode | None = None
    ):
        """
        Set fieldsets to control the layout of admin “add” and “change” pages.
        fieldsets is a list of two-tuples, in which each two-tuple represents a <fieldset>
        on the admin form page. (A <fieldset> is a “section” of the form.)
        """
        fieldsets: list[tuple[str, dict]] = []
        if not getattr(obj, "node_type", None):
            warnings.warn("Expected a 'Node' with a 'NodeType' in the admin form")

        if not obj:
            # This default form is returned before a field
            # type is selected
            return super().get_fieldsets(request, obj)
        try:
            node = obj.get_node()
        except Exception as E:
            warnings.warn(f"{E}")
            return fieldsets
        if isinstance(node, formkit_schema.FormKitSchemaProps) and not isinstance(
            node, (formkit_schema.GroupNode, formkit_schema.FormKitSchemaDOMNode, formkit_schema.RepeaterNode)
        ):
            # Field validation applies to formkit
            # except repeater and group
            fieldsets.append(
                (
                    "Field Validation",
                    {
                        "fields": (
                            "validation",
                            "validationLabel",
                            "validationVisibility",
                            "validationMessages",
                            "validationRules",
                        )
                    },
                )
            )
        elif isinstance(node, formkit_schema.RepeaterNode):
            if obj.node and obj.node.get("formkit", None) == "repeater":
                fieldsets.append(
                    (
                        "Repeater field properties",
                        {"fields": ("addLabel", "upControl", "downControl", "itemsClass", "itemClass")},
                    )
                )

        grouped_fields = reduce(operator.or_, (set(opts["fields"]) for _, opts in fieldsets), set())
        # Add 'ungrouped' fields
        fieldsets.insert(
            0, (None, {"fields": [field for field in self.get_fields(request, obj) if field not in grouped_fields]})
        )
        logger.info(fieldsets)
        return fieldsets

    def get_form(
        self,
        request: HttpRequest,
        obj: models.FormKitSchemaNode | None,
        change: bool,
        **kwargs,
    ) -> type[forms.ModelForm[Any]]:
        if not obj:
            return NewFormKitForm
        try:
            node = obj.get_node()
        except Exception as E:
            warnings.warn(f"{E}")
            return NewFormKitForm
        if isinstance(node, formkit_schema.GroupNode):
            return FormKitNodeGroupForm
        elif isinstance(node, formkit_schema.RepeaterNode):
            return FormKitNodeRepeaterForm
        elif isinstance(node, formkit_schema.FormKitSchemaDOMNode):
            return FormKitElementForm
        elif isinstance(node, formkit_schema.FormKitSchemaComponent):
            return FormKitComponentForm
        elif isinstance(node, formkit_schema.FormKitSchemaCondition):
            return FormKitConditionForm
        elif isinstance(node, formkit_schema.FormKitSchemaProps):
            return FormKitNodeForm

        else:
            warnings.warn(f"Unable to determine form type for {obj}")
            return super().get_form(request, obj, change, **kwargs)


@admin.register(models.FormKitSchema)
class FormKitSchemaAdmin(OrderedInlineModelAdminMixin, admin.ModelAdmin):
    form = FormKitSchemaForm

    def get_inlines(self, request, obj: models.FormKitSchema | None):
        """
        For a "new object" do not show the Form Components
        """
        if not obj:
            return []
        return [
            FormKitSchemaComponentInline,
        ]

    inlines = [
        FormKitSchemaComponentInline,
    ]


@admin.register(models.FormComponents)
class FormComponentsAdmin(OrderedModelAdmin):
    list_display = ("label", "schema", "node", "move_up_down_links")


class OptionLabelInline(admin.TabularInline):
    model = models.OptionLabel
    extra = 0


class OptionInline(admin.TabularInline):
    model = models.Option
    extra = 0
    fields = ("group", "object_id", "value", "field")
    readonly_fields = ("group", "object_id", "value", "field")


@admin.register(models.Option)
class OptionAdmin(OrderedModelAdmin):
    list_display = ("object_id", "value", "field", "order", "group", "move_up_down_links")
    inlines = [OptionLabelInline]
    list_select_related = ("group",)
    readonly_fields = ("group", "object_id", "value", "field", "created_by", "updated_by")


@admin.register(models.OptionGroup)
class OptionGroupAdmin(admin.ModelAdmin):
    inlines = [OptionInline]
    ...


@admin.register(models.OptionLabel)
class OptionLabelAdmin(admin.ModelAdmin):
    list_display = (
        "label",
        "lang",
    )
    readonly_fields = ("option",)
    search_fields = ("label",)
