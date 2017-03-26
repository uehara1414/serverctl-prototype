from datetime import timedelta
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Game(models.Model):
    name = models.CharField('ゲーム名', max_length=32)

    def __str__(self):
        return self.name


class GameServerGroup(models.Model):
    name = models.CharField('ゲームサーバーの名前', max_length=32)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    cost_per_hour = models.PositiveIntegerField('１時間あたりのランニングコスト')

    def save(self, *args, **kwargs):
        super(GameServerGroup, self).save(*args, **kwargs)


class GameServer(models.Model):
    INITIALIZING = 'INITIALIZING'
    LOADING = 'LOADING'
    RUNNING = 'RUNNING'
    SAVING = 'SAVING'
    STOPPING = 'STOPPING'
    STATUS_CHOICES = (
        (INITIALIZING, '準備中'),
        (LOADING, '起動中'),
        (RUNNING, '作動中'),
        (SAVING, '保存中'),
        (STOPPING, '停止中'),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(default=timezone.now)
    group = models.ForeignKey(GameServerGroup, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=12,
        choices=STATUS_CHOICES,
        default=STOPPING,
    )

    class Meta:
        get_latest_by = "created_at"

    def start(self):
        """とりあえず、待ち時間を飛ばしてRunningに"""
        self.started_at = timezone.now()

        self.status = self.LOADING
        ServerHistory.objects.create(server=self, status=self.LOADING)

        self.status = self.RUNNING
        ServerHistory.objects.create(server=self, status=self.RUNNING)

        self.save()

    def stop(self):
        """とりあえず、待ち時間を飛ばしてStoppingに"""

        self.status = self.SAVING
        ServerHistory.objects.create(server=self, status=self.SAVING)

        self.status = self.STOPPING
        ServerHistory.objects.create(server=self, status=self.STOPPING)

        players = Player.objects.filter(group=self.group)
        amount = self.calc_payment() // len(players)
        for player in players:
            Payments.objects.create(player=player, amount=amount)
        self.save()

    def calc_payment(self):
        hours = (timezone.now() - self.started_at).seconds // 60 // 60 + 1
        return self.group.cost_per_hour * hours


class ServerHistory(models.Model):
    server = models.ForeignKey(GameServer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=12,
        choices=GameServer.STATUS_CHOICES,
    )


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


class Payments(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    player = models.ForeignKey(Player)
    amount = models.IntegerField(default=0)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.player.user.username}: {self.amount}円 {self.paid}'
