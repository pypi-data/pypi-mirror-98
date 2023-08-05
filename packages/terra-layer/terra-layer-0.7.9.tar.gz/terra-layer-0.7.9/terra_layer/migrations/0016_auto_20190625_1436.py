# Generated by Django 2.0.13 on 2019-06-25 12:36

import json

import django.contrib.postgres.fields.jsonb
from django.db import migrations


def set_json_defaults(apps, schema_editor):
    Layer = apps.get_model("terra_layer", "Layer")
    for layer in Layer.objects.all():
        try:
            json.loads(layer.legend_template)
        except json.JSONDecodeError:
            layer.legend_template = "[]"
            layer.save()


class Migration(migrations.Migration):

    dependencies = [("terra_layer", "0015_remove_filterfield_filter_type")]

    operations = [
        migrations.RunPython(set_json_defaults),
        migrations.AlterField(
            model_name="layer",
            name="legend_template",
            field=django.contrib.postgres.fields.jsonb.JSONField(default=list),
        ),
    ]
