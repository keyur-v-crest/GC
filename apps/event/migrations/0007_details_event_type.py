# Generated by Django 5.0.2 on 2024-03-14 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0006_details_organizer_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='details',
            name='event_type',
            field=models.BooleanField(default=False),
        ),
    ]
