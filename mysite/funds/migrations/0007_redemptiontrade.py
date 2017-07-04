# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-04 05:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('funds', '0006_remove_pruchasetrade_ack_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='RedemptionTrade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('redemption_date', models.DateField()),
                ('redemption_share_amount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('redemption_fee', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('net_price', models.DecimalField(decimal_places=4, default=0, max_digits=6)),
                ('benefit_amount', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='benefit amount')),
                ('fund', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='funds.Fund')),
            ],
        ),
    ]
