# Generated by Django 3.2.7 on 2021-09-29 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='questions',
            fields=[
                ('question', models.CharField(max_length=30)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('general', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
    ]
