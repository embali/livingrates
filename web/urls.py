from django.conf.urls import url

from .views import Web, Map, Search


urlpatterns = [
    url(r'^$', Web.as_view(), name='web'),
    url(r'^search/$', Search.as_view(), name='search'),
    url(r'^map/$', Map.as_view(), name='map'), ]
