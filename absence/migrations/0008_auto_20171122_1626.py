# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-11-22 14:26
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('absence', '0007_auto_20171113_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='pickFrom',
            field=models.CharField(default=datetime.datetime(2017, 11, 22, 14, 26, 13, 293833, tzinfo=utc), max_length=200),
        ),
        migrations.AlterField(
            model_name='leave',
            name='pickTo',
            field=models.CharField(default=datetime.datetime(2017, 11, 22, 14, 26, 13, 293869, tzinfo=utc), max_length=200),
        ),
    ]
