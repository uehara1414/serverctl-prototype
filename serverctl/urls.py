from django.conf.urls import url

from .views import index
from .views import mypage
from .views import login_view
from .views import signup
from .views import new_server_group
from .views import add_player
from .views import server_group_detail
from .views import player_detail
from .views import start_server
from .views import stop_server


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^mypage/$', mypage, name='mypage'),
    url(r'^login/$', login_view, name='login'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^new_server_group/$', new_server_group, name='new_server_group'),
    url(r'^server_group/(?P<pk>[0-9]+)/$', server_group_detail, name='server_group_detail'),
    url(r'^add_player/$', add_player, name='add_player'),
    url(r'^player_detail/(?P<pk>[0-9]+)/$', player_detail, name='player_detail'),
    url(r'^start_server/(?P<pk>[0-9]+)/$', start_server, name='start_server'),
    url(r'^stop_server/(?P<pk>[0-9]+)/$', stop_server, name='stop_server'),
]
