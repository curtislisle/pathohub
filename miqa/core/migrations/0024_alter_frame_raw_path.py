# Generated by Django 3.2.10 on 2022-01-19 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_user_identified_artifacts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frame',
            name='raw_path',
            field=models.CharField(max_length=500),
        ),
    ]
