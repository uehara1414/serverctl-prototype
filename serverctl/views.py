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

from .forms import GameServerForm


@login_required
def index(request):
    return render(request, 'serverctl/index.html')


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


def new_server(request):

    if request.method == 'POST':
        game_server = GameServerForm(request.POST)
        game_server.save()
        return redirect(reverse('serverctl:index'))

    else:
        form = GameServerForm()
        return render(request, 'serverctl/new_server.html', {'form': form})
