# Generated by Django 5.0.2 on 2024-02-19 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_details_relation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='details',
            name='email_otp',
            field=models.CharField(default=None, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='details',
            name='email_otp_expier',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='details',
            name='mobile_otp',
            field=models.CharField(default=None, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='details',
            name='mobile_otp_expier',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]
