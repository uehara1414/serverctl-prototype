# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-12 00:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serverctl', '0006_paymenthistory_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='serverhistory',
            name='data_s3_key',
            field=models.CharField(default='', max_length=64),
        ),
    ]
