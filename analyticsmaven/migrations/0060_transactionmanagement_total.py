# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-06 13:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyticsmaven', '0059_transactionmanagement_released'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionmanagement',
            name='total',
            field=models.FloatField(default=0.0),
        ),
    ]
