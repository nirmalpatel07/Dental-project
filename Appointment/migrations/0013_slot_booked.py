# Generated by Django 5.0.2 on 2024-02-19 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Appointment', '0012_remove_appointment_am_pm'),
    ]

    operations = [
        migrations.AddField(
            model_name='slot',
            name='booked',
            field=models.BooleanField(default=False),
        ),
    ]
