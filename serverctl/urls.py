from django.conf.urls import url

from .views import index
from .views import login_view
from .views import signup
from .views import new_server_group
from .views import add_player
from .views import server_group_detail
from .views import player_detail


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^login/$', login_view, name='login'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^new_server_group/$', new_server_group, name='new_server_group'),
    url(r'^server_group/(?P<pk>[0-9]+)/$', server_group_detail, name='server_group_detail'),
    url(r'^add_player/$', add_player, name='add_player'),
    url(r'^player_detail/(?P<pk>[0-9]+)/$', player_detail, name='player_detail'),
]
