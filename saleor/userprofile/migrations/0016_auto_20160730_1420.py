# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-07-30 19:20
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0015_auto_20160730_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='phone',
            field=models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(message='Invalid phone number', regex='^\\+?1?\\d{6,12}$')], verbose_name='phone number'),
        ),
    ]
