# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-28 09:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyticsmaven', '0032_auto_20180828_0935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationlist',
            name='type',
            field=models.CharField(blank=True, choices=[('Applied Job', 'Applied Job'), ('Approved Job', 'Approved Job'), ('Completed Job', 'Completed Job'), ('Pending Job', 'Pending Job'), ('Closed Job', 'Closed Job'), ('Chat', 'Chat')], max_length=20, null=True, verbose_name='Notification Type'),
        ),
    ]
