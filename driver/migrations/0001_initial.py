# Generated by Django 4.2 on 2023-06-07 10:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('donor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('DeliveryID', models.AutoField(primary_key=True, serialize=False)),
                ('PickupCode', models.CharField(default='00000', max_length=5)),
                ('Status', models.CharField(choices=[('future', 'future'), ('delivered', 'delivered'), ('intransit', 'intransit')], default='future', max_length=10)),
                ('PickupDateTime', models.DateTimeField()),
                ('Destination', models.CharField(max_length=255)),
                ('DonationID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donor.donation')),
            ],
            options={
                'verbose_name': 'delivery',
                'verbose_name_plural': 'deliveries',
            },
        ),
    ]
