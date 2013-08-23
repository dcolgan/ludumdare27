from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import *
from game.models import *
from util.functions import *
import math
import ipdb

class Account(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(blank=True)
    color = models.CharField(max_length=10, blank=True)
    leader_name = models.CharField(max_length=255, blank=True)
    people_name = models.CharField(max_length=255, blank=True)
    unplaced_units = models.IntegerField(default=0)

    is_staff = models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.')
    is_active = models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')

    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'account'
        verbose_name_plural = 'accounts'

    def __unicode__(self):
        return self.username

    def get_username(self):
        return self.username

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.username

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])


#class SquareOccupiedException(Exception):
#    pass
#class InvalidPlacementException(Exception):
#    pass
#class SquareDoesNotExistException(Exception):
#    pass




#class ObjectManager(models.Manager):
#    def method(self):
#        pass
#
#class Object(models.Model):
#    owner = models.ForeignKey(Account, related_name='units')
#    square = models.ForeignKey(Square, related_name='units')
#    amount = models.IntegerField()
#    last_turn_amount = models.IntegerField(default=0)
#
#    objects = ObjectManager()
#
#    def __unicode__(self):
#        return unicode(self.square)

