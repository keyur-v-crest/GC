# Generated by Django 5.0.2 on 2024-02-21 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='details',
            name='event_delete',
            field=models.BooleanField(default=False),
        ),
    ]
