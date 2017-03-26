from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import GameServer
from .models import GameServerGroup
from .models import Player

from .forms import GameServerGroupForm
from .forms import AddPlayerForm


@login_required
def index(request):
    servers = GameServerGroup.objects.all()
    return render(request, 'serverctl/index.html', {'servers': servers})


def login_view(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(reverse('serverctl:index'))
            return redirect(reverse('serverctl:login'))
    logout(request)
    return render(request, 'serverctl/login.html')


def signup(request):
    print(request.POST)
    if request.method == 'POST':
        user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
        print(user)
        authenticate(username=request.POST['username'], password=request.POST['password'])
        login(request, user)
        return redirect(reverse('serverctl:index'))
    return redirect('/login/')


@login_required
def new_server_group(request):

    if request.method == 'POST':
        game_group = GameServerGroupForm(request.POST)
        group = game_group.save()
        GameServer.objects.create(group=group)
        Player.objects.create(user=request.user, group=group, roll=Player.OWNER)
        return redirect(reverse('serverctl:index'))

    else:
        form = GameServerGroupForm()
        return render(request, 'serverctl/new_server.html', {'form': form})


@login_required
def server_group_detail(request, pk):
    group = GameServerGroup.objects.get(id=pk)
    players = Player.objects.filter(group=group)
    server = GameServer.objects.filter(group=group).latest()
    add_player_form = AddPlayerForm()
    context = {
        'server_group': group,
        'players': players,
        'server': server,
        'add_player_form': add_player_form
    }
    return render(request, 'serverctl/server_group_detail.html', context)


def add_player(request):
    if request.method == 'POST':
        player = AddPlayerForm(request.POST)
        player = player.save()
        return redirect(f'/server_group/{player.group.pk}/')


def player_detail(request, pk):
    user = Player.objects.get(pk=pk).user
    players = Player.objects.filter(user=user)
    return render(request, 'serverctl/player_detail.html', {'players': players})


def start_server(request, pk):
    server = GameServer.objects.get(pk=pk)
    server.start()
    return redirect(f'/server_group/{server.group.pk}/')
