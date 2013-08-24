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
            login(request, account)

            #send_templated_mail(
            #    template_name='registration-confirmation',
            #    from_email=settings.ADMIN_EMAIL_SENDER,
            #    recipient_list=[account.email],
            #    context={
            #        'domain': settings.SITE_DOMAIN,
            #        'account': account,
            #    })
            return HttpResponseRedirect(reverse('settings'))

    else:
        form = CreateAccountForm()
    return render(request, 'create-account.html', locals())

@login_required
def game(request):
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

#@login_required
#@api_view(['GET'])
#def api_sector(request, col, row, width, height):
#    try:
#        col = int(col)
#        row = int(row)
#        width = int(width)
#        height = int(height)
#    except:
#        raise Http404
#
#    # TODO a lot of this function can be computed on the turn change and then cached, do this if we get a bunch of traffic
#    # TODO make this instead limit it to a few screens beyond where the furthest person is
#    if (col > MAX_SECTOR_X * SECTOR_SIZE or
#       col < MIN_SECTOR_X * SECTOR_SIZE or
#       row > MAX_SECTOR_Y * SECTOR_SIZE or
#       row < MIN_SECTOR_Y * SECTOR_SIZE):
#        return Response({
#            'error': 'I really don\'t feel like fetching the map that far out.'
#        }, status=status.HTTP_400_BAD_REQUEST)
#
#    if width > 200 or height > 200:
#        return Response({
#            'error': 'Yo dog, you can\'t seriously have a screen that big.  If you do, let the admin know though and I\'ll increase the max screen size.'
#        }, status=status.HTTP_400_BAD_REQUEST)
#
#    if width < 1 or height < 1:
#        return Response({
#            'error': 'What is this, a quantum computer?  Your screen size must be expressed in positive numbers.'
#        }, status=status.HTTP_400_BAD_REQUEST)
#
#    squares = Square.objects.get_region(col, row, width, height)
#
#    is_initial = (
#        Unit.objects.filter(owner=request.user).count() == 0 and
#        Square.objects.filter(owner=request.user).count() == 0
#    )
#
#    return Response(SquareSerializer(squares, many=True).data)

@login_required
@api_view(['GET'])
def api_initial_load(request):
    #moves = Move.objects.filter(player=request.user).filter(turn=current_turn)

    return Response({
        #'moves': MoveSerializer(moves, many=True).data,
        'account': AccountSerializer(request.user).data,
    })
    
#@login_required
#@api_view(['POST'])
#def api_square_unit_action(request, src_col, src_row, dest_col, dest_row, kind, amount):
#    try:
#        src_col = int(src_col)
#        src_row = int(src_row)
#        dest_col = int(dest_col)
#        dest_row = int(dest_row)
#    except:
#        raise Http404
#
#    if new_move.is_valid():
#        new_move.save()
#    else:
#        return Response({'error': new_move.error}, status=status.HTTP_400_BAD_REQUEST)
