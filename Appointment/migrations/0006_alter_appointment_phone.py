# Generated by Django 5.0.2 on 2024-02-19 15:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Appointment', '0005_alter_appointment_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='phone',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^[0-9]*$', 'Only numeric digits are allowed.')]),
        ),
    ]
