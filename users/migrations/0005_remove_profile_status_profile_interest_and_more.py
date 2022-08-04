# Generated by Django 4.0.6 on 2022-08-02 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_profile_age'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='status',
        ),
        migrations.AddField(
            model_name='profile',
            name='interest',
            field=models.TextField(blank=True, default='NO INFO'),
        ),
        migrations.AddField(
            model_name='profile',
            name='programmingLanguage',
            field=models.TextField(blank=True, default='NO INFO'),
        ),
    ]