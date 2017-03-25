from django.conf.urls import url

from .views import index
from .views import login_view
from .views import signup
from .views import new_server_group


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^login/$', login_view, name='login'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^new_server_group/$', new_server_group, name='new_server_group'),
]
