# Generated by Django 4.2 on 2023-06-07 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0005_remove_delivery_distancetraveled_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='DistanceTraveled',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='delivery',
            name='TimeSpentOnRoad',
            field=models.DurationField(blank=True, null=True),
        ),
    ]