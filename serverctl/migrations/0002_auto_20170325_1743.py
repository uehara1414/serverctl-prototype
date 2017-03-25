# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-25 17:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serverctl', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gameserver',
            name='cost_per_hour',
        ),
        migrations.RemoveField(
            model_name='gameserver',
            name='name',
        ),
        migrations.AddField(
            model_name='gameservergroup',
            name='cost_per_hour',
            field=models.PositiveIntegerField(default=1, verbose_name='１時間あたりのランニングコスト'),
            preserve_default=False,
        ),
    ]
