from django.contrib import admin
from .models import Game
from .models import GameServer
from .models import GameServerGroup
from .models import Player
from .models import Payments
from .models import ServerHistory

# Register your models here.
admin.site.register(Game)
admin.site.register(GameServerGroup)
admin.site.register(GameServer)
admin.site.register(Player)
admin.site.register(Payments)
admin.site.register(ServerHistory)
