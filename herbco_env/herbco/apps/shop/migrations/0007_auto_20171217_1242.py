# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-17 09:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0006_itemextra_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_items',
            field=models.ManyToManyField(related_name='order_items', to='shop.Item'),
        ),
        migrations.AddField(
            model_name='order',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]