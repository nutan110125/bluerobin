# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-04 11:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyticsmaven', '0050_transactionmanagement_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionmanagement',
            name='status',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('COMPLETED', 'COMPLETED')], default='PENDING', max_length=15, verbose_name='Payment Status'),
        ),
    ]
