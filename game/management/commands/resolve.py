from django.core.management.base import BaseCommand, CommandError
from game.models import *
import random

class Command(BaseCommand):
    args = ''
    help = 'Run this command whenever 2 minutes go by.'

    def handle(self, *args, **options):
        Announcement.objects.all().delete()

        RED_START = { 'col': 14, 'row': 14 }
        BLUE_START = { 'col': 36, 'row': 61 }

        all_actions = {}
        player_locations = {}
        for account in Account.objects.all():
            if account.actions != '':
                this_accounts_actions = []
                actions = account.actions.split(',')

                for action in actions:
                    if action == 'walk':
                        this_accounts_actions.append('walk-start')
                        this_accounts_actions.append('walk')

                    else:
                        this_accounts_actions.append(action)

                if len(this_accounts_actions) < 10:
                    for i in range(10 - len(this_accounts_actions)):
                        this_accounts_actions.append('rest')
                all_actions[account.id] = this_accounts_actions

            else:
                all_actions[account.id] = ['rest']*10

            account.last_chat_message = account.chat_message
            account.chat_message = ''
            account.last_actions = account.actions
            account.last_col = account.col
            account.last_row = account.row
            account.last_direction = account.direction
            account.actions = ''
            account.save()

        print 'Action hash setup complete.'

        print all_actions

        for second in range(10):
            for account in Account.objects.all():
                this_action_name = all_actions[account.id][second]
                if this_action_name != 'walk-start':

                    # Figure stamina for this action
                    this_action = get_action_by_name(this_action_name)
                    account.stamina += this_action['stamina']
                    if account.stamina > 10:
                        account.stamina = 10

                    if this_action_name == 'walk':
                        if account.direction == 'west':
                            account.col -= 1
                        if account.direction == 'east':
                            account.col += 1
                        if account.direction == 'north':
                            account.row -= 1
                        if account.direction == 'south':
                            account.row += 1

                        # Give flags to those who should have them
                        square = get_object_or_None(Square, col=account.col, row=account.row)
                        if square != None:
                            if TILES[square.tile] == 'red-flag' and account.team == 'blue':
                                account.has_flag = True
                            if TILES[square.tile] == 'blue-flag' and account.team == 'red':
                                account.has_flag = True

                            if (account.has_flag and square.col < 25 and account.team == 'red') or (account.has_flag and square.col >= 25 and account.team == 'blue'):
                                account.has_flag = False
                                account.flags_gotten += 1
                                Announcement.objects.create(text='%s gets a flag for %s' % (account.username, account.get_team_display()))

                    if this_action_name == 'run':

                        # Factor this into a function sometime
                        if account.direction == 'west':
                            account.col -= 1
                        if account.direction == 'east':
                            account.col += 1
                        if account.direction == 'north':
                            account.row -= 1
                        if account.direction == 'south':
                            account.row += 1

                        # Give flags to those who should have them
                        square = get_object_or_None(Square, col=account.col, row=account.row)
                        if square != None:
                            if TILES[square.tile] == 'red-flag' and account.team == 'blue':
                                account.has_flag = True
                            if TILES[square.tile] == 'blue-flag' and account.team == 'red':
                                account.has_flag = True

                            if (account.has_flag and square.col < 25 and account.team == 'red') or (account.has_flag and square.col >= 25 and account.team == 'blue'):
                                account.has_flag = False
                                account.flags_gotten += 1
                                Announcement.objects.create(text='%s gets a flag for %s' % (account.username, account.get_team_display()))

                        if account.direction == 'west':
                            account.col -= 1
                        if account.direction == 'east':
                            account.col += 1
                        if account.direction == 'north':
                            account.row -= 1
                        if account.direction == 'south':
                            account.row += 1

                        # Give flags to those who should have them
                        square = get_object_or_None(Square, col=account.col, row=account.row)
                        if square != None:
                            if TILES[square.tile] == 'red-flag' and account.team == 'blue':
                                account.has_flag = True
                            if TILES[square.tile] == 'blue-flag' and account.team == 'red':
                                account.has_flag = True

                            if (account.has_flag and square.col < 25 and account.team == 'red') or (account.has_flag and square.col >= 25 and account.team == 'blue'):
                                account.has_flag = False
                                account.flags_gotten += 1
                                Announcement.objects.create(text='%s gets a flag for %s' % (account.username, account.get_team_display()))



                    if this_action_name in ['north', 'south', 'east', 'west']:
                        account.direction = this_action_name

                    account.save()


                if account.col not in player_locations:
                    player_locations[account.col] = {}
                
                if account.row not in player_locations[account.col]:
                    player_locations[account.col][account.row] = []

                player_locations[account.col][account.row].append(account)

        print 'Action resolutions finished'

#        print 'Action resolutions finished'
#
#        for row in range(75):
#            for col in range(50):
#                players_in_this_square = player_locations[col][row]
#                if len(players_in_this_square) > 2:
#                    for account in players_in_this_square:
#                        for other_account in players_in_this_square:
#                            if account != other_account:
#                                if account.team != other_account.team:
#                                    if col < 25:
#                                        if account.team == 'blue':
#                                            account.col = BLUE_START['col']
#                                            account.row = BLUE_START['row']
#                                        if other_account.team == 'blue':
#                                            account.col = BLUE_START['col']
#                                            account.row = BLUE_START['row']
#                                    else:
#                                        if account.team == 'red':
#                                            account.col = RED_START['col']
#                                            account.row = RED_START['row']
#                                        if other_account.team == 'red':
#                                            account.col = RED_START['col']
#                                            account.row = RED_START['row']
