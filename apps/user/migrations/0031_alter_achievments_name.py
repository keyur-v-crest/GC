# Generated by Django 5.0.2 on 2024-03-27 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0030_achievments_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achievments',
            name='name',
            field=models.JSONField(default=dict),
        ),
    ]
