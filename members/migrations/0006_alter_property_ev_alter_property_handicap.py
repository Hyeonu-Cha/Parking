# Generated by Django 4.1.7 on 2023-03-14 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0005_alter_property_ev_alter_property_handicap'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='ev',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='property',
            name='handicap',
            field=models.BooleanField(),
        ),
    ]
