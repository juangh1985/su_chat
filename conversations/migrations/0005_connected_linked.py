# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-12-18 22:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversations', '0004_auto_20171218_2101'),
    ]

    operations = [
        migrations.AddField(
            model_name='connected',
            name='linked',
            field=models.BooleanField(default=False, max_length=3, verbose_name='linked'),
            preserve_default=False,
        ),
    ]
