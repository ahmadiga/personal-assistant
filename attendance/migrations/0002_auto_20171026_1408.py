# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-10-26 11:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='duration',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
