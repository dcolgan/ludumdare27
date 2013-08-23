from django.conf.urls import patterns, include, url
from django.conf import settings
from rest_framework.generics import *
from game.models import *
from game.views import *

urlpatterns = patterns('game.views',
    url(r'^$', 'home', name='home'),

    url(r'^game/$', 'game', name='game'),

    url(r'^create-account/$', 'create_account', name='create-account'),

    #url(r'^profile/$', 'profile', name='profile'),
    #url(r'^profile/(?P<account_id>\d+)/$', 'profile', name='profile'),

    #url(r'^api/sector/(?P<col>[0-9-]+)/(?P<row>[0-9-]+)/(?P<width>[0-9]+)/(?P<height>[0-9]+)/$', 'api_sector', name='api-sector'),
    #url(r'^api/square/(?P<col>[0-9-]+)/(?P<row>[0-9-]+)/(?P<kind>move|attack|city)/(?P<amount>\d)/$', 'api_square_unit_action', name='api-square-unit-action'),

    url(r'^api/initial-load/$', 'api_initial_load', name='api-initial-load'),

)
