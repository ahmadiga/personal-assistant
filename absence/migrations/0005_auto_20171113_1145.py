# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-11-13 09:45
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('absence', '0004_auto_20171112_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='pickFrom',
            field=models.CharField(default=datetime.datetime(2017, 11, 13, 9, 45, 1, 922149, tzinfo=utc), max_length=200),
        ),
        migrations.AlterField(
            model_name='leave',
            name='pickTo',
            field=models.CharField(default=datetime.datetime(2017, 11, 13, 9, 45, 1, 922186, tzinfo=utc), max_length=200),
        ),
    ]
