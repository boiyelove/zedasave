# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-07 17:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zerasaver', '0026_remove_usersavingsplan_time_of_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersavingsplan',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
