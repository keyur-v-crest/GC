# Generated by Django 5.0.2 on 2024-02-16 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='details',
            name='address',
            field=models.CharField(default=None, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='details',
            name='dob',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AddField(
            model_name='details',
            name='family_id',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AddField(
            model_name='details',
            name='gender',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='details',
            name='profession',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AddField(
            model_name='details',
            name='profession_description',
            field=models.CharField(default=None, max_length=500),
        ),
    ]
