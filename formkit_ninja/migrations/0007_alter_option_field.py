# Generated by Django 4.2.1 on 2023-08-28 05:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("formkit_ninja", "0006_option_group_option_unique_option_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="option",
            name="field",
            field=models.ForeignKey(
                blank=True,
                help_text="The ID of an Option node (select, dropdown or radio) if this option is embedded as part of a selection node",
                limit_choices_to={"node__formkit__in": ["select", "radio", "dropdown"]},
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="formkit_ninja.formkitschemanode",
            ),
        ),
    ]
