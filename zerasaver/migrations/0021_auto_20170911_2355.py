# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-11 22:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('zerasaver', '0020_auto_20170911_2353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersavingsplan',
            name='active_sub',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='zerasaver.USubscriptions'),
        ),
    ]
