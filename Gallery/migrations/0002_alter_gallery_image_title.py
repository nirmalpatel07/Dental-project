# Generated by Django 5.0.2 on 2024-02-21 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gallery', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='image_title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
