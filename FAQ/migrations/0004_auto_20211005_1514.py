# Generated by Django 3.2.7 on 2021-10-05 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FAQ', '0003_auto_20211005_1508'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='questions',
            options={'ordering': ('-id',), 'verbose_name': 'Вопросы'},
        ),
        migrations.AlterModelOptions(
            name='relation_question',
            options={'verbose_name': 'Таблица связей вопросов'},
        ),
    ]