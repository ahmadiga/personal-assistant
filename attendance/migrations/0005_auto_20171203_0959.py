# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-12-03 07:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0004_auto_20171203_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='duration',
            field=models.BigIntegerField(blank=True, default=0, null=True),
        ),
    ]
