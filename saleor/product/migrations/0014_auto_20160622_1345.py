# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-06-22 18:45
from __future__ import unicode_literals

from django.db import migrations
import django_prices.models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_auto_20160218_0812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=django_prices.models.PriceField(currency='BGN', decimal_places=2, max_digits=12, verbose_name='price'),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='price_override',
            field=django_prices.models.PriceField(blank=True, currency='BGN', decimal_places=2, max_digits=12, null=True, verbose_name='price override'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='cost_price',
            field=django_prices.models.PriceField(blank=True, currency='BGN', decimal_places=2, max_digits=12, null=True, verbose_name='cost price'),
        ),
    ]
