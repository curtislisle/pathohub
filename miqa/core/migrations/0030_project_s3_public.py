# Generated by Django 3.2.12 on 2022-04-12 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_project_email_recipients'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='s3_public',
            field=models.BooleanField(
                default=False, help_text='Whether the S3 bucket is publicly readable.'
            ),
        ),
    ]
