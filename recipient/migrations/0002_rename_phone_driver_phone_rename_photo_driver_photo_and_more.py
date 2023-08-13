# Generated by Django 4.2.2 on 2023-08-12 08:44

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import recipient.models


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0003_remove_donation_pickuptime_donation_status_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipient', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='driver',
            old_name='Phone',
            new_name='phone',
        ),
        migrations.RenameField(
            model_name='driver',
            old_name='Photo',
            new_name='photo',
        ),
        migrations.RemoveField(
            model_name='recipientdelivery',
            name='Destination',
        ),
        migrations.AddField(
            model_name='organization',
            name='Status',
            field=models.CharField(choices=[('Unverified', 'Unverified'), ('Verified', 'Verified')], default='Unverified', max_length=10),
        ),
        migrations.AddField(
            model_name='recipientdelivery',
            name='ManagerID',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='recipient', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='driver',
            name='Status',
            field=models.CharField(choices=[('idle', 'idle'), ('onDelivery', 'onDelivery')], default='idle', max_length=10),
        ),
        migrations.AlterField(
            model_name='organization',
            name='Photo',
            field=models.ImageField(default=recipient.models.default_ngo_photo, upload_to='organization_photos/'),
        ),
        migrations.AlterField(
            model_name='recipientdelivery',
            name='DeliveryID',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='recipientdelivery',
            name='Status',
            field=models.CharField(choices=[('pending', 'pending'), ('delivered', 'delivered'), ('Intransit', 'Intransit')], default='pending', max_length=10),
        ),
        migrations.CreateModel(
            name='OrganizationRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rated_entity_type', models.CharField(choices=[('ORGANIZATION', 'Organization')], max_length=20)),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5.0)])),
                ('donation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='donor.donation')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organizationrating', to='recipient.organization')),
                ('restaurant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='donor.restaurant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
