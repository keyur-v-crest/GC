# Generated by Django 5.0.2 on 2024-03-24 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='details',
            name='type',
            field=models.CharField(default=None, max_length=1000),
        ),
    ]
