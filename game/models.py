from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import *
from game.models import *
from util.functions import *
import math
import ipdb

class Account(AbstractBaseUser, PermissionsMixin):
    TEAMS = (
        ('red', 'red'),
        ('blue', 'blue'),
    )
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(blank=True)
    team = models.CharField(max_length=2, choices=TEAMS, blank=True)
    has_flag = models.BooleanField(default=False)
    col = models.IntegerField(null=True, blank=True)
    row = models.IntegerField(null=True, blank=True)

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


#class SquareOccupiedException(Exception):
#    pass
#class InvalidPlacementException(Exception):
#    pass
#class SquareDoesNotExistException(Exception):
#    pass




#class ObjectManager(models.Manager):
#    def method(self):
#        pass


class Move(models.Model):
    MOVE_CHOICES = (
        ('walk', 'Walk'),
        ('run', 'Run'),
        ('left', 'Turn Left'),
        ('right', 'Turn Right'),
        ('reverse', 'Turn Around'),
    )
    account = models.ForeignKey(Account, related_name='moves')
    next = models.ForeignKey('self', blank=True, null=True, related_name='previous')
    which = models.CharField(max_length=10, choices=MOVE_CHOICES)
    

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
