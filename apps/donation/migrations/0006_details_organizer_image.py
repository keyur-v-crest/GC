# Generated by Django 5.0.2 on 2024-03-26 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0005_remove_details_location_details_donation_city_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='details',
            name='organizer_image',
            field=models.CharField(default=None, max_length=1000, null=True),
        ),
    ]
