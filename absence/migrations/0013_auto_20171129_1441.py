# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-11-29 12:41
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('absence', '0012_auto_20171129_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='pickFrom',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 29, 12, 41, 3, 600207, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='leave',
            name='pickTo',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 29, 12, 41, 3, 600313, tzinfo=utc)),
        ),
    ]
