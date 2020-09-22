# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-07-31 14:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_auto_20160622_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description_bg',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='category',
            name='description_en_us',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='category',
            name='name_bg',
            field=models.CharField(max_length=128, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='category',
            name='name_en_us',
            field=models.CharField(max_length=128, null=True, verbose_name='name'),
        ),
    ]