from django import forms

from .models import Game
from .models import GameServer
from .models import GameServerGroup
from .models import Player


class GameServerForm(forms.ModelForm):
    class Meta:
        model = GameServer
        exclude = ('status', )
