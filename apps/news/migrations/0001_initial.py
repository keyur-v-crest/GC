# Generated by Django 5.0.2 on 2024-03-14 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Details',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.CharField(default=None, max_length=1000)),
                ('name', models.CharField(default=None, max_length=200)),
                ('news_type', models.CharField(default=None, max_length=100)),
            ],
        ),
    ]
