# Generated by Django 5.0.2 on 2024-03-22 09:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
        ('donation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='details',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='category.details'),
        ),
    ]
