from django.shortcuts import render, get_object_or_404
from django.db.models import F
from django.contrib import messages 
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import *
from django.shortcuts import _get_queryset
from game.models import *
from game.serializers import *
from game.forms import *
from util.functions import *
from django.contrib.auth import authenticate, login

from rest_framework.generics import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.utils import simplejson
import random
import math
import ipdb

import datetime

def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('game'))
    return render(request, 'home.html', locals())

def create_account(request):
    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            form.save()
            account = authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])
            account.col = 24
            account.row = 37
            account.team = random.choice(['red', 'blue'])
            account.save()
            login(request, account)

            #send_templated_mail(
            #    template_name='registration-confirmation',
            #    from_email=settings.ADMIN_EMAIL_SENDER,
            #    recipient_list=[account.email],
            #    context={
            #        'domain': settings.SITE_DOMAIN,
            #        'account': account,
            #    })
            return HttpResponseRedirect(reverse('game'))
    else:
        form = CreateAccountForm()
    return render(request, 'create-account.html', locals())

@login_required
def game(request):
    rows = []
    span = 7

    for row in range(request.user.row-span, request.user.row+span+1):
        squares = (Square.objects.
            filter(col__gte=request.user.col-span).
            filter(col__lte=request.user.col+span).
            filter(row=row).
            order_by('col'))
        rows.append(squares)

    return render(request, 'game.html', locals())

class AccountAPIView(RetrieveAPIView, ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AccountSerializer
    model = Account

@login_required
@api_view(['GET'])
def api_username_existence(request, username):
    taken = (get_object_or_None(Account, username=username) != None)
    return Response({ 'taken': taken })

@login_required
@api_view(['GET'])
def api_email_existence(request, email):
    taken = (get_object_or_None(Account, email=email) != None)
    return Response({ 'taken': taken })

@login_required
@api_view(['POST'])
def api_action(request, action):
    if request.user.actions == '':
        current_actions = []
    else:
        current_actions = request.user.actions.split(',')

    total_seconds = 0
    for current_action in current_actions:
        print current_action
        total_seconds += get_action_by_name(current_action)['seconds']

    if total_seconds + get_action_by_name(action)['seconds'] > 10:
        return Response({
            'error': 'You do not have enough seconds to add that action.'
        }, status=status.HTTP_400_BAD_REQUEST)

    current_actions.append(action)
    request.user.actions = ','.join(current_actions)
    request.user.save()

    return Response('')

@login_required
@api_view(['POST'])
def api_cancel(request, move_position):
    move_position = int(move_position)
    current_actions = request.user.actions.split(',')

    if current_actions != '' and (move_position < 0 or move_position >= len(current_actions)):
        return Response({
            'error': 'Invalid cancel.'
        }, status=status.HTTP_400_BAD_REQUEST)

    del current_actions[move_position]
    request.user.actions = ','.join(current_actions)
    request.user.save()


    return Response('')

@login_required
@api_view(['GET'])
def api_initial_load(request):

    span = 7
    other_players = (
        Account.objects.
            filter(col__gte=request.user.col-span).
            filter(col__lte=request.user.col+span).
            filter(row__gte=request.user.row-span).
            filter(row__lte=request.user.row+span).
            exclude(pk=request.user.id)
    )

    return Response({
        'action_data': ACTIONS,
        'user_actions': request.user.actions,
        'account': AccountSerializer(request.user).data,
        'other_players': AccountSerializer(other_players, many=True).data,
    })
