# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-07 05:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analyticsmaven', '0018_auto_20180807_0547'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobseeker',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='job_seeker_country', to='analyticsmaven.Country'),
        ),
        migrations.AddField(
            model_name='jobseeker',
            name='timezone',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='job_seeker_timezone', to='analyticsmaven.Timezone'),
        ),
        migrations.AddField(
            model_name='jobseeker',
            name='week_availability',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='job_seeker_hours', to='analyticsmaven.Hours'),
        ),
    ]
