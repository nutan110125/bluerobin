# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-02 07:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyticsmaven', '0011_auto_20180801_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatlist',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
