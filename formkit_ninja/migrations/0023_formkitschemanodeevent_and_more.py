# Generated by Django 4.2.6 on 2023-10-25 18:05

import uuid

import django.db.models.deletion
import pgtrigger.compiler
import pgtrigger.migrations
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("pghistory", "0006_delete_aggregateevent"),
        ("formkit_ninja", "0022_formkitschemanode_soft_delete"),
    ]

    operations = [
        migrations.CreateModel(
            name="FormKitSchemaNodeEvent",
            fields=[
                ("pgh_id", models.AutoField(primary_key=True, serialize=False)),
                ("pgh_created_at", models.DateTimeField(auto_now_add=True)),
                ("pgh_label", models.TextField(help_text="The event label.")),
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, serialize=False)),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "node_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("$cmp", "Component"),
                            ("text", "Text"),
                            ("condition", "Condition"),
                            ("$formkit", "FormKit"),
                            ("$el", "Element"),
                            ("raw", "Raw JSON"),
                        ],
                        max_length=256,
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        help_text="Decribe the type of data / reason for this component",
                        max_length=4000,
                        null=True,
                    ),
                ),
                (
                    "label",
                    models.CharField(
                        blank=True, help_text="Used as a human-readable label", max_length=1024, null=True
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "node",
                    models.JSONField(
                        blank=True, help_text="A JSON representation of select parts of the FormKit schema", null=True
                    ),
                ),
                (
                    "additional_props",
                    models.JSONField(blank=True, help_text="User space for additional, less used props", null=True),
                ),
                (
                    "text_content",
                    models.TextField(
                        blank=True,
                        help_text="Content for a text element, for children of an $el type component",
                        null=True,
                    ),
                ),
                ("track_change", models.BigIntegerField(blank=True, null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="formkitschemanode",
            trigger=pgtrigger.compiler.Trigger(
                name="insert_insert",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    func='INSERT INTO "formkit_ninja_formkitschemanodeevent" ("additional_props", "created", "created_by_id", "description", "id", "is_active", "label", "node", "node_type", "option_group_id", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "text_content", "track_change", "updated", "updated_by_id") VALUES (NEW."additional_props", NEW."created", NEW."created_by_id", NEW."description", NEW."id", NEW."is_active", NEW."label", NEW."node", NEW."node_type", NEW."option_group_id", _pgh_attach_context(), NOW(), \'insert\', NEW."id", NEW."text_content", NEW."track_change", NEW."updated", NEW."updated_by_id"); RETURN NULL;',
                    hash="534b4b21d7cf93a9105cdc2c791147f3365be30d",
                    operation="INSERT",
                    pgid="pgtrigger_insert_insert_72c4c",
                    table="formkit_ninja_formkitschemanode",
                    when="AFTER",
                ),
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="formkitschemanode",
            trigger=pgtrigger.compiler.Trigger(
                name="update_update",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    condition="WHEN (OLD.* IS DISTINCT FROM NEW.*)",
                    func='INSERT INTO "formkit_ninja_formkitschemanodeevent" ("additional_props", "created", "created_by_id", "description", "id", "is_active", "label", "node", "node_type", "option_group_id", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "text_content", "track_change", "updated", "updated_by_id") VALUES (NEW."additional_props", NEW."created", NEW."created_by_id", NEW."description", NEW."id", NEW."is_active", NEW."label", NEW."node", NEW."node_type", NEW."option_group_id", _pgh_attach_context(), NOW(), \'update\', NEW."id", NEW."text_content", NEW."track_change", NEW."updated", NEW."updated_by_id"); RETURN NULL;',
                    hash="0154bfb8e2197684b693fce5fec3631e30fa5537",
                    operation="UPDATE",
                    pgid="pgtrigger_update_update_d7c99",
                    table="formkit_ninja_formkitschemanode",
                    when="AFTER",
                ),
            ),
        ),
        migrations.AddField(
            model_name="formkitschemanodeevent",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                related_query_name="+",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="formkitschemanodeevent",
            name="option_group",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                related_query_name="+",
                to="formkit_ninja.optiongroup",
            ),
        ),
        migrations.AddField(
            model_name="formkitschemanodeevent",
            name="pgh_context",
            field=models.ForeignKey(
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="pghistory.context",
            ),
        ),
        migrations.AddField(
            model_name="formkitschemanodeevent",
            name="pgh_obj",
            field=models.ForeignKey(
                db_constraint=False,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="events",
                to="formkit_ninja.formkitschemanode",
            ),
        ),
        migrations.AddField(
            model_name="formkitschemanodeevent",
            name="updated_by",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                related_query_name="+",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
