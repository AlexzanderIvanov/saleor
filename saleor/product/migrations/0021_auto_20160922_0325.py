# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-22 08:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0020_auto_20160922_0304'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['order', 'id'], 'verbose_name_plural': 'categories'},
        ),
    ]
