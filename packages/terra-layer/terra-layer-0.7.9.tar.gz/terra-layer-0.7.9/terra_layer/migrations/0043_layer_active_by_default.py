# Generated by Django 2.2.5 on 2019-11-12 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("terra_layer", "0042_auto_20191105_0307"),
    ]

    operations = [
        migrations.AddField(
            model_name="layer",
            name="active_by_default",
            field=models.BooleanField(default=False),
        ),
    ]
