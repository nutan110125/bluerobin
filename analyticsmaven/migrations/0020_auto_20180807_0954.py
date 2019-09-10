# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-07 09:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyticsmaven', '0019_auto_20180807_0549'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobmanagement',
            name='country',
        ),
        migrations.AddField(
            model_name='jobmanagement',
            name='country',
            field=models.ManyToManyField(blank=True, null=True, related_name='job_country', to='analyticsmaven.Country'),
        ),
    ]
