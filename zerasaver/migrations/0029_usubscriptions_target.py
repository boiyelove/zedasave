# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-08 09:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zerasaver', '0028_auto_20171008_0916'),
    ]

    operations = [
        migrations.AddField(
            model_name='usubscriptions',
            name='target',
            field=models.PositiveIntegerField(default=2),
        ),
    ]
