# Generated by Django 3.2.7 on 2021-12-19 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FAQ', '0013_alter_settings_bot_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings_bot',
            name='bot_name',
            field=models.CharField(default='Укажите название бота', max_length=50, verbose_name='Название бота'),
        ),
    ]