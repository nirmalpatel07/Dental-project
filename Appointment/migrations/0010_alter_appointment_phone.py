# Generated by Django 5.0.2 on 2024-02-19 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Appointment', '0009_alter_appointment_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='phone',
            field=models.CharField(max_length=15),
        ),
    ]
