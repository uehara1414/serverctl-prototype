from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    name = models.CharField('ゲーム名', max_length=32)


class GameServer(models.Model):
    LOADING = 'LOADING'
    RUNNING = 'RUNNING'
    SAVING = 'SAVING'
    STOPPING = 'STOPPING'
    STATUS_CHOICES = (
        (LOADING, '起動中'),
        (RUNNING, '作動中'),
        (SAVING, '保存中'),
        (STOPPING, '停止中'),
    )
    name = models.CharField('ゲームサーバーの名前', max_length=32)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    cost_per_hour = models.PositiveIntegerField('１時間あたりのランニングコスト')
    status = models.CharField(
        max_length=12,
        choices=STATUS_CHOICES,
        default=STOPPING,
    )


class GameServerGroup(models.Model):
    name = models.CharField('ゲームサーバーの名前', max_length=32)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    server = models.ForeignKey(GameServer, on_delete=models.CASCADE)


class Player(models.Model):
    OWNER = 'OWNER'
    ADMIN = 'ADMIN'
    NORMAL = 'NORMAL'
    ROLL_CHOICES = (
        (OWNER, '作成者'),
        (ADMIN, '管理者'),
        (NORMAL, '一般'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(GameServerGroup, on_delete=models.CASCADE)
    roll = models.CharField(
        max_length=6,
        choices=ROLL_CHOICES,
        default=NORMAL,
    )
