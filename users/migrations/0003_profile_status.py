# Generated by Django 4.0.6 on 2022-08-01 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_image_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='status',
            field=models.TextField(default='NO INFO'),
        ),
    ]
