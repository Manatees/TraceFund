# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 03:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funds', '0002_auto_20170628_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fundhistory',
            name='netprice',
            field=models.DecimalField(decimal_places=4, max_digits=6, verbose_name='net price'),
        ),
    ]
