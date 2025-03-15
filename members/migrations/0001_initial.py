# Generated by Django 4.1.7 on 2023-03-12 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('admin', models.BooleanField()),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=20)),
                ('f_name', models.CharField(max_length=20)),
                ('l_name', models.CharField(max_length=20)),
                ('mobile', models.IntegerField()),
                ('bankaccount', models.CharField(blank=True, max_length=20, null=True)),
                ('birth', models.DateField()),
            ],
        ),
    ]
