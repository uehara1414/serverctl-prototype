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

from .forms import GameServerGroupForm
from .models import GameServer
from .models import GameServerGroup
from .models import Player


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
        game_group.save()
        return redirect(reverse('serverctl:index'))

    else:
        form = GameServerGroupForm()
        return render(request, 'serverctl/new_server.html', {'form': form})
