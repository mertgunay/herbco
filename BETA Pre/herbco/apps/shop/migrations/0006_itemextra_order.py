# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-17 09:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_item_related_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemExtra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('itemex', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='itemex', to='shop.Item')),
                ('shopcart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.ShoppingCart')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]