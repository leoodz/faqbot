# Generated by Django 3.2.7 on 2022-01-19 14:38

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('FAQ', '0016_alter_settings_bot_status'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='relation_question',
            new_name='RelationQuestion',
        ),
        migrations.RenameModel(
            old_name='settings_bot',
            new_name='SettingsBot',
        ),
    ]
