# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-17 13:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_item_is_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_items',
            field=models.ManyToManyField(blank=True, related_name='order_items', to='shop.Item'),
        ),
    ]
