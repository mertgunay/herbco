# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-17 11:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_auto_20171217_1242'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
