# Generated by Django 3.2.7 on 2021-09-29 20:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('FAQ', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='answer',
            field=models.TextField(default='No text'),
        ),
        migrations.CreateModel(
            name='relation_question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Основной_вопрос', to='FAQ.questions')),
                ('sub', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Дополнительный_вопрос', to='FAQ.questions')),
            ],
        ),
    ]
