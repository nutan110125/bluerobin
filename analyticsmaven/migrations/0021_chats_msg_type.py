# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-07 12:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyticsmaven', '0020_auto_20180807_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='chats',
            name='msg_type',
            field=models.CharField(default='text', max_length=20, verbose_name='Type'),
        ),
    ]
