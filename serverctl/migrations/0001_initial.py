# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-25 17:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='ゲーム名')),
            ],
        ),
        migrations.CreateModel(
            name='GameServer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='ゲームサーバーの名前')),
                ('cost_per_hour', models.PositiveIntegerField(verbose_name='１時間あたりのランニングコスト')),
                ('status', models.CharField(choices=[('LOADING', '起動中'), ('RUNNING', '作動中'), ('SAVING', '保存中'), ('STOPPING', '停止中')], default='STOPPING', max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='GameServerGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='ゲームサーバーの名前')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serverctl.Game')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roll', models.CharField(choices=[('OWNER', '作成者'), ('ADMIN', '管理者'), ('NORMAL', '一般')], default='NORMAL', max_length=6)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serverctl.GameServerGroup')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='gameserver',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serverctl.GameServerGroup'),
        ),
    ]
