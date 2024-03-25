# Generated by Django 5.0.2 on 2024-03-24 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0009_rename_event_type_details_is_vip_seat_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='details',
            name='organizer_image',
        ),
        migrations.AddField(
            model_name='details',
            name='event_address_city',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='details',
            name='event_address_state',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]
