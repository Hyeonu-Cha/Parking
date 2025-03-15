# Generated by Django 4.1.7 on 2023-03-12 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='admin',
        ),
        migrations.RemoveField(
            model_name='user',
            name='id',
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default='000', max_length=20, primary_key=True, serialize=False, unique=True),
            preserve_default=False,
        ),
    ]
