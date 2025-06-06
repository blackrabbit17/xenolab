# Generated by Django 5.2.1 on 2025-05-10 01:58

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TempHumidityReading',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('temperature', models.FloatField(help_text='Temperature value in Celsius')),
                ('humidity', models.FloatField(help_text='Humidity value in percentage')),
            ],
        ),
    ]
