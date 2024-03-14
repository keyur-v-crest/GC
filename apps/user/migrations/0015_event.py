# Generated by Django 5.0.2 on 2024-03-14 05:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_booking_gallery'),
        ('user', '0014_alter_details_profession_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('family_id', models.CharField(default=None, max_length=100, null=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.details')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
