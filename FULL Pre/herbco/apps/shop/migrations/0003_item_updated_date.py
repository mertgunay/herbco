# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-06 09:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_item_is_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
