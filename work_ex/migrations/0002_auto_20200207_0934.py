# Generated by Django 3.0.3 on 2020-02-07 04:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_ex', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='workex',
            name='present_job',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='workex',
            name='end_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='workex',
            name='start_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
