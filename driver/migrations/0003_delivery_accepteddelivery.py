# Generated by Django 4.2 on 2023-06-07 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='AcceptedDelivery',
            field=models.BooleanField(default=False),
        ),
    ]