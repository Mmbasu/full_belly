# Generated by Django 4.2.2 on 2023-08-13 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_customuser_password_reset_token_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='delete_account_code',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
