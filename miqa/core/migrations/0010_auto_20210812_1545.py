# Generated by Django 3.2.5 on 2021-08-12 15:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0009_session_lock_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='lock_owner',
        ),
        migrations.AddField(
            model_name='experiment',
            name='lock_owner',
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='experiment_locks',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
