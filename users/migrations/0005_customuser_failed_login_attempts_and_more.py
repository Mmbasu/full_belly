# Generated by Django 4.2.2 on 2023-09-04 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_customuser_delete_account_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='failed_login_attempts',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='customuser',
            name='last_login_attempt_exceeded',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
