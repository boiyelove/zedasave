# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-09 13:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zerasaver', '0012_auto_20170809_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersavingsplan',
            name='deposit_time',
            field=models.CharField(max_length=8, null=True),
        ),
    ]
