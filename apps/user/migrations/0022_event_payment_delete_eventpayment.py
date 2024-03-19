# Generated by Django 5.0.2 on 2024-03-19 08:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djstripe', '0012_2_8'),
        ('user', '0021_eventpayment'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='payment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_event_payment', to='djstripe.webhookeventtrigger'),
        ),
        migrations.DeleteModel(
            name='EventPayment',
        ),
    ]
