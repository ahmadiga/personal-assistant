# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-12-03 09:35
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('performance', '0009_auto_20171203_0959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performance',
            name='year',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 12, 3, 9, 35, 17, 674212, tzinfo=utc), null=True),
        ),
    ]
