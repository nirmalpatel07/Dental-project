# Generated by Django 5.0.2 on 2024-02-15 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_service_service_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='service_image',
            field=models.FileField(default=None, max_length=250, null=True, upload_to='media/%y'),
        ),
    ]
