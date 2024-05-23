# Generated by Django 5.0.2 on 2024-03-24 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dentist',
            name='user',
        ),
        migrations.AddField(
            model_name='dentist',
            name='first_name',
            field=models.CharField(default='om', max_length=100),
        ),
        migrations.AddField(
            model_name='dentist',
            name='last_name',
            field=models.CharField(default='om', max_length=100),
        ),
    ]