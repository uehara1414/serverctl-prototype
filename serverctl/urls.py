from django.conf.urls import url

from .views import index
from .views import login_view
from .views import signup
from .views import new_server


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^login/$', login_view, name='login'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^new_server/$', new_server, name='new_server'),
]
