# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-25 18:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serverctl', '0002_auto_20170325_1743'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gameserver',
            options={'get_latest_by': 'created_at'},
        ),
        migrations.AddField(
            model_name='gameserver',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]