# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-07-17 17:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0011_auto_20160717_0428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='postal_code',
            field=models.CharField(max_length=20, verbose_name='postal code'),
        ),
    ]
