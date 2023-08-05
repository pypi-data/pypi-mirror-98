# Generated by Django 2.2.8 on 2020-01-06 12:50

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import terra_layer.schema
import uuid


def create_uuid(apps, schema_editor):
    Layer = apps.get_model("terra_layer", "Layer")
    for inst in Layer.objects.all():
        inst.uuid = uuid.uuid4()
        inst.save()


class Migration(migrations.Migration):

    dependencies = [
        ("terra_layer", "0046_migrate_layer_groups_2_tree"),
    ]

    operations = [
        migrations.AddField(
            model_name="layer",
            name="uuid",
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.RunPython(create_uuid, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="layer",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name="scene",
            name="tree",
            field=django.contrib.postgres.fields.jsonb.JSONField(
                default=list,
                validators=[
                    terra_layer.schema.JSONSchemaValidator(
                        limit_value={
                            "$id": "http://terralego.com/scene_layertree.json",
                            "$schema": "http://json-schema.org/draft-07/schema#",
                            "definitions": {},
                            "items": {
                                "$id": "#/items",
                                "dependencies": {"group": ["children", "label"]},
                                "properties": {
                                    "children": {"$ref": "#"},
                                    "expanded": {
                                        "$id": "#/items/properties/expanded",
                                        "default": False,
                                        "examples": [True],
                                        "title": "The expanded status in admin. Not used yet",
                                        "type": "boolean",
                                    },
                                    "geolayer": {
                                        "$id": "#/items/properties/geolayer",
                                        "default": 0,
                                        "examples": [96],
                                        "title": "The geolayer id",
                                        "type": "integer",
                                    },
                                    "group": {
                                        "$id": "#/items/properties/exclusive",
                                        "default": False,
                                        "examples": [True],
                                        "title": "Is the group exclusive ?",
                                        "type": "boolean",
                                    },
                                    "label": {
                                        "$id": "#/items/properties/label",
                                        "default": "",
                                        "examples": ["My Group"],
                                        "pattern": "^(.*)$",
                                        "title": "The group name",
                                        "type": "string",
                                    },
                                    "selectors": {
                                        "$id": "#/items/properties/selectors",
                                        "title": "The selectors for this group",
                                        "type": ["array", "null"],
                                    },
                                    "settings": {
                                        "$id": "#/items/properties/settings",
                                        "title": "The settings of group",
                                        "type": "object",
                                    },
                                },
                                "required": [],
                                "title": "Layer tree item",
                                "type": "object",
                            },
                            "title": "Scene layer tree schema",
                            "type": "array",
                        }
                    )
                ],
            ),
        ),
    ]
