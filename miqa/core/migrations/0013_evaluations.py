# Generated by Django 3.2.7 on 2021-09-21 12:58

import uuid

from django.db import migrations, models
import django.db.models.deletion


def default_evaluation_model_mapping():
    return {'ncanda-t1spgr-v1': 'MIQAT1-0', 'ncanda-mprage-v1': 'MIQAT1-0'}


class Migration(migrations.Migration):

    replaces = [
        ('core', '0013_auto_20210917_1235'),
        ('core', '0014_evaluation'),
        ('core', '0015_alter_evaluation_image'),
    ]

    dependencies = [
        ('core', '0012_alter_experiment_lock_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='evaluation_models',
            field=models.JSONField(default=default_evaluation_model_mapping),
        ),
        migrations.AlterField(
            model_name='scan',
            name='scan_type',
            field=models.CharField(
                choices=[
                    ('ncanda-t1spgr-v1', 'ncanda-t1spgr-v1'),
                    ('ncanda-mprage-v1', 'ncanda-mprage-v1'),
                ],
                max_length=255,
            ),
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ('evaluation_model', models.CharField(max_length=50)),
                ('results', models.JSONField()),
                (
                    'image',
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.image'),
                ),
            ],
        ),
    ]
