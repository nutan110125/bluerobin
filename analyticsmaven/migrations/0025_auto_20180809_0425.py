# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-09 04:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyticsmaven', '0024_auto_20180809_0424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='sign_up',
            field=models.CharField(choices=[('Analytics Maven', 'Analytics Maven'), ('linkedin-oauth2', 'Linked In'), ('google-oauth2', 'Google'), ('facebook-oauth2', 'Facebook')], default='Analytics Maven', max_length=20, verbose_name='SignUp Type'),
        ),
    ]
