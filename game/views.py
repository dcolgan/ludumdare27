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
from django.db.models import Count, Min, Sum, Avg

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

def how_to_play(request):
    return render(request, 'how-to-play.html', locals())

def leaderboards(request):
    top_taggers = Account.objects.order_by('-enemies_tagged')[:20]
    top_flag_getters = Account.objects.order_by('-flags_gotten')[:20]

    red_flags = Account.objects.filter(team='red').aggregate(red_flags=Sum('flags_gotten'))['red_flags']
    blue_flags = Account.objects.filter(team='blue').aggregate(blue_flags=Sum('flags_gotten'))['blue_flags']

    red_tags = Account.objects.filter(team='red').aggregate(red_tags=Sum('enemies_tagged'))['red_tags']
    blue_tags = Account.objects.filter(team='blue').aggregate(blue_tags=Sum('enemies_tagged'))['blue_tags']

    return render(request, 'leaderboards.html', locals())

def create_account(request):
    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            form.save()
            account = authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])
            account.team = random.choice(['red', 'blue'])
            if account.team == 'red':
                account.col = 20
                account.row = 37
            else:
                account.col = 30
                account.row = 37

            account.last_col = account.col
            account.last_row = account.row
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
            return HttpResponseRedirect(reverse('how-to-play'))
    else:
        form = CreateAccountForm()
    return render(request, 'create-account.html', locals())

@login_required
def game(request):
    rows = []
    col_span = 10
    row_span = 8

    announcements = Announcement.objects.all()

    for row in range(request.user.row-row_span, request.user.row+row_span+1):
        squares = (Square.objects.
            filter(col__gte=request.user.col-col_span).
            filter(col__lte=request.user.col+col_span).
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
    prev_actions_stamina = 0
    for current_action in current_actions:
        this_action = get_action_by_name(current_action)
        total_seconds += this_action['seconds']
        prev_actions_stamina += this_action['stamina']

    if total_seconds + get_action_by_name(action)['seconds'] > 10:
        return Response({
            'error': 'You do not have enough seconds to add that action.'
        }, status=status.HTTP_400_BAD_REQUEST)

    if request.user.stamina + prev_actions_stamina + get_action_by_name(action)['stamina'] < 0:
        return Response({
            'error': 'You do not have enough stamina to add that action.'
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

    current_actions = current_actions[:move_position] # Delete all moves after this one also
    request.user.actions = ','.join(current_actions)
    request.user.save()

    return Response('')

@login_required
@api_view(['POST'])
def api_update_chat(request):
    request.user.chat_message = request.DATA['message']
    request.user.save()

    return Response('')

@login_required
@api_view(['GET'])
def api_initial_load(request):

    col_span = 10
    row_span = 8
    other_players = (
        Account.objects.
            filter(col__gte=request.user.col-col_span).
            filter(col__lte=request.user.col+col_span).
            filter(row__gte=request.user.row-row_span).
            filter(row__lte=request.user.row+row_span).
            exclude(pk=request.user.id)
    )

    return Response({
        'action_data': ACTIONS,
        'user_actions': request.user.actions,
        'account': AccountSerializer(request.user).data,
        'other_players': AccountSerializer(other_players, many=True).data,
    })
