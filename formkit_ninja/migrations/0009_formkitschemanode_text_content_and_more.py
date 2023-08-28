# Generated by Django 4.2.1 on 2023-08-28 06:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("formkit_ninja", "0008_remove_option_label"),
    ]

    operations = [
        migrations.AddField(
            model_name="formkitschemanode",
            name="text_content",
            field=models.TextField(
                blank=True, help_text="Content for a text element, for children of an $el type component", null=True
            ),
        ),
        migrations.AlterField(
            model_name="nodechildren",
            name="parent",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="formkit_ninja.formkitschemanode"),
        ),
    ]
