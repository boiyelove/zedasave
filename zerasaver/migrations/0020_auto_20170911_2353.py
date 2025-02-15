# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-11 22:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('zerasaver', '0019_auto_20170911_2212'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersavingsplan',
            name='has_auth',
        ),
        migrations.RemoveField(
            model_name='usersavingsplan',
            name='psub_code',
        ),
        migrations.RemoveField(
            model_name='usersavingsplan',
            name='psub_id',
        ),
        migrations.RemoveField(
            model_name='usersavingsplan',
            name='psub_token',
        ),
        migrations.AddField(
            model_name='usersavingsplan',
            name='active_sub',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='zerasaver.USubscriptions'),
        ),
    ]
