from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import *
from game.models import *
from util.functions import *
import math
import ipdb

class Account(AbstractBaseUser, PermissionsMixin):
    TEAMS = (
        ('red', 'Red'),
        ('blue', 'Blue'),
    )
    DIRECTIONS = (
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    )
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(blank=True)
    team = models.CharField(max_length=5, choices=TEAMS, blank=True)
    has_flag = models.BooleanField(default=False)
    col = models.IntegerField(null=True, blank=True)
    row = models.IntegerField(null=True, blank=True)
    last_col = models.IntegerField(null=True, blank=True)
    last_row = models.IntegerField(null=True, blank=True)
    last_direction = models.CharField(max_length=10, choices=DIRECTIONS, blank=True, default='south')
    direction = models.CharField(max_length=10, choices=DIRECTIONS, blank=True, default='south')
    last_chat_message = models.CharField(max_length=75, blank=True, default='')
    chat_message = models.CharField(max_length=75, blank=True, default='')
    inactive_turns = models.IntegerField(default=0)

    flags_gotten = models.IntegerField(default=0)
    enemies_tagged = models.IntegerField(default=0)

    actions = models.CharField(max_length=255, default='', blank=True)
    last_actions = models.CharField(max_length=255, default='', blank=True)
    stamina = models.IntegerField(default=10)


    is_staff = models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.')
    is_active = models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')

    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

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

ACTIONS = [
    { 'which': 'rest', 'name': 'Rest', 'seconds': 1, 'stamina': 1, 'icon': 'glyphicon-pause' },
    { 'which': 'walk', 'name': 'Walk', 'seconds': 2, 'stamina': 0, 'icon': 'glyphicon-step-forward' },
    { 'which': 'run', 'name': 'Run', 'seconds': 1, 'stamina': -2, 'icon': 'glyphicon-fast-forward' },
    { 'which': 'north', 'name': 'Face North', 'seconds': 1, 'stamina': 0, 'icon': 'glyphicon-chevron-up' },
    { 'which': 'south', 'name': 'Face South', 'seconds': 1, 'stamina': 0, 'icon': 'glyphicon-chevron-down' },
    { 'which': 'east', 'name': 'Face East', 'seconds': 1, 'stamina': 0, 'icon': 'glyphicon-chevron-right' },
    { 'which': 'west', 'name': 'Face West', 'seconds': 1, 'stamina': 0, 'icon': 'glyphicon-chevron-left' },
]
def get_action_by_name(which):
    for action in ACTIONS:
        if action['which'] == which:
            return action


TILES = [
    None,
    'grass', 'water', 'corn', 'rocks', 'trees', None, None, None, None, None,
    'grass', 'shrubbery', 'grass', 'grass', None, None, None, None, None, None,
    'road', 'road', 'red-flag', 'blue-flag', None, None, None, None, None, None,
    'road', 'road', 'water', 'water', None, None, None, None, None, None,
    'road', 'road', 'water', 'water', None, None, None, None, None, None,
    'road', 'road', None, None, None, None, None, None, None, None,
    'road', 'road', None, None, None, None, None, None, None, None,
    'road', 'road', None, None, None, None, None, None, None, None,
    'road', 'road', None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None, None, None,

]

#class SquareOccupiedException(Exception):
#    pass
#class InvalidPlacementException(Exception):
#    pass
#class SquareDoesNotExistException(Exception):
#    pass




#class ObjectManager(models.Manager):
#    def method(self):
#        pass

RED_START = { 'col': 14, 'row': 14 }
BLUE_START = { 'col': 36, 'row': 61 }

    

class Square(models.Model):
    TERRAIN_TYPES = (
        ('grass', 'grass'),
        ('dirt', 'dirt'),
        ('water', 'water'),
        ('corn', 'corn'),
        ('tree', 'tree'),
        ('rock', 'rock'),
        ('building', 'building'),
        ('shrubbery', 'shrubbery'),
        ('road', 'road'),
    )
    col = models.IntegerField()
    row = models.IntegerField()
    terrain_type = models.CharField(max_length=10, choices=TERRAIN_TYPES)
    tile = models.IntegerField()

    def get_css_offset_x(self):

        return str(32 * (self.tile-1) % 320 * -1) + 'px'
    def get_css_offset_y(self):
        return str(32 * (self.tile-1) / 320 * 32 * -1) + 'px'

    def get_terrain_type(self):
        return TILES[self.tile]

class Log(models.Model):
    TEAMS = (
        ('red', 'Red'),
        ('blue', 'Blue'),
    )
    col = models.IntegerField()
    row = models.IntegerField()
    team = models.CharField(max_length=5, choices=TEAMS)
    has_flag = models.BooleanField(default=False)


class Announcement(models.Model):
    text = models.CharField(max_length=75)
