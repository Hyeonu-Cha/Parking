# Generated by Django 4.1.7 on 2023-03-23 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0009_requestmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestmodel',
            name='property_image',
            field=models.ImageField(blank=True, null=True, upload_to='property_images/'),
        ),
    ]
