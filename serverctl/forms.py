from django import forms

from .models import Game
from .models import GameServer
from .models import GameServerGroup
from .models import Player


class GameServerGroupForm(forms.ModelForm):
    class Meta:
        model = GameServerGroup
        fields = ('name', 'game', 'cost_per_hour')
