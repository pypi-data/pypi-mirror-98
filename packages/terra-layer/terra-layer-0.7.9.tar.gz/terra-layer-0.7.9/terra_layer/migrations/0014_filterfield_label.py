# Generated by Django 2.0.13 on 2019-06-24 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("terra_layer", "0013_auto_20190620_1455")]

    operations = [
        migrations.AddField(
            model_name="filterfield",
            name="label",
            field=models.CharField(blank=True, max_length=255),
        )
    ]
