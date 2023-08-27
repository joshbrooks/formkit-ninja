# Generated by Django 4.2.1 on 2023-08-27 23:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    replaces = [
        ("formkit_ninja", "0004_alter_formcomponents_label"),
        ("formkit_ninja", "0005_alter_formkitschemanode_label"),
        ("formkit_ninja", "0006_formkitschema_label_alter_formkitschema_key"),
        ("formkit_ninja", "0007_remove_formkitschema_key"),
        ("formkit_ninja", "0008_remove_formkitschemanode_translation_context"),
        ("formkit_ninja", "0009_alter_formcomponents_node"),
    ]

    dependencies = [
        ("formkit_ninja", "0003_delete_translatable"),
    ]

    operations = [
        migrations.AlterField(
            model_name="formcomponents",
            name="label",
            field=models.CharField(blank=True, help_text="Used as a human-readable label", max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name="formkitschemanode",
            name="label",
            field=models.CharField(blank=True, help_text="Used as a human-readable label", max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name="formkitschema",
            name="label",
            field=models.TextField(blank=True, help_text="Used as a human-readable label", null=True),
        ),
        migrations.RemoveField(
            model_name="formkitschema",
            name="key",
        ),
        migrations.RemoveField(
            model_name="formkitschemanode",
            name="translation_context",
        ),
        migrations.AlterField(
            model_name="formcomponents",
            name="node",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="formkit_ninja.formkitschemanode",
            ),
        ),
    ]
