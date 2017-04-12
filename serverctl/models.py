from datetime import timedelta
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
from serverctl import minecraft
from threading import Thread
from serverctl_prototype.utils import slack


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
    ip = models.CharField(max_length=64, default='')

    class Meta:
        get_latest_by = "created_at"

    def _generate_id(self):
        return f'{self.group.game.name}-{str(uuid.uuid4())}'

    def _start(self):
        slack.send('loading')
        id = self._generate_id()
        self.started_at = timezone.now()

        self.status = self.LOADING
        ServerHistory.objects.create(server=self, status=self.LOADING, data_s3_key=id)
        self.save()

        slack.send(id)
        minecraft.start_new_server(id)
        self.ip = minecraft.get_drpolet_ip(id)

        self.status = self.RUNNING
        ServerHistory.objects.create(server=self, status=self.RUNNING, data_s3_key=id)

        self.save()
        slack.send('created')

    def start(self):
        Thread(target=self._start, daemon=True).start()

    def _stop(self):
        last = ServerHistory.objects.filter(server=self).latest()
        self.status = self.SAVING
        ServerHistory.objects.create(server=self, status=self.SAVING, data_s3_key=last.data_s3_key)
        self.save()

        minecraft.stop(last.data_s3_key)

        self.status = self.STOPPING
        ServerHistory.objects.create(server=self, status=self.STOPPING, data_s3_key=last.data_s3_key)

        players = Player.objects.filter(group=self.group)
        amount = self.calc_payment() // len(players)
        for player in players:
            Payments.objects.create(player=player, group=self.group, amount=amount)
        self.save()

    def stop(self):
        Thread(target=self._stop, daemon=True).start()

    def calc_payment(self):
        hours = (timezone.now() - self.started_at).seconds // 60 // 60 + 1
        return self.group.cost_per_hour * hours


class ServerHistory(models.Model):
    server = models.ForeignKey(GameServer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    data_s3_key = models.CharField(max_length=64, default='')
    status = models.CharField(
        max_length=12,
        choices=GameServer.STATUS_CHOICES,
    )

    class Meta:
        get_latest_by = "created_at"


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
    group = models.ForeignKey(GameServerGroup)
    amount = models.IntegerField(default=0)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.player.user.username}: {self.amount}円 {self.paid}'

    def save(self, *args, **kwargs):
        super(Payments, self).save(*args, **kwargs)
        if not self.paid:
            type = PaymentHistory.CREATED
        else:
            type = PaymentHistory.PAID
        PaymentHistory.objects.create(payment=self, type=type)


class PaymentHistory(models.Model):
    CREATED = 'CREATED'
    PAID = 'PAID'
    TYPE_CHOICES = (
        (CREATED, '請求'),
        (PAID, '決済'),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    payment = models.ForeignKey(Payments)
    type = models.CharField(
        max_length=12,
        choices=TYPE_CHOICES
    )
