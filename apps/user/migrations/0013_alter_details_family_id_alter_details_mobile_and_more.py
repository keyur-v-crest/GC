# Generated by Django 5.0.2 on 2024-02-21 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_details_is_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='details',
            name='family_id',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='details',
            name='mobile',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='details',
            name='profession',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]
