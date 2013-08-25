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

    url(r'^api/action/(?P<action>rest|walk|run|north|south|east|west)/$', 'api_action', name='api-action'),
    url(r'^api/cancel/(?P<move_position>\d+)/$', 'api_cancel', name='api-cancel'),

    url(r'^api/initial-load/$', 'api_initial_load', name='api-initial-load'),

)
