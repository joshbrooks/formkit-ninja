# Generated by Django 4.2.6 on 2023-10-16 14:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("formkit_ninja", "0020_remove_formcomponents_order_on_update_option_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="formkitschemanode",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]
