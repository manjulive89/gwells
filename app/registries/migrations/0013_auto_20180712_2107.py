# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-12 21:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registries', '0012_auto_20180704_2105'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='registriesapplication',
            options={'ordering': ['primary_certificate_no'], 'verbose_name_plural': 'Applications'},
        ),
    ]
