# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-12-03 07:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0003_auto_20171026_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='duration',
            field=models.BigIntegerField(blank=True, default=None, null=True),
        ),
    ]
