from django.core.management.base import BaseCommand, CommandError
from game.models import *
import settings
from PIL import Image
import random

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    if lv == 1:
        v = int(value, 16)*17
        return v, v, v
    if lv == 3:
        return tuple(int(value[i:i+1], 16)*17 for i in range(0, 3))
    return tuple(int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3))

class Command(BaseCommand):
    args = ''
    help = 'Run this command whenever 2 minutes go by.'

    def handle(self, *args, **options):
        Announcement.objects.all().delete()

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
                        this_accounts_actions.append('noop')
                all_actions[account.id] = this_accounts_actions

                account.inactive_turns = 0
            else:
                all_actions[account.id] = ['noop']*10
                account.inactive_turns += 1

            account.last_chat_message = account.chat_message
            account.chat_message = ''
            account.last_actions = account.actions
            account.last_col = account.col
            account.last_row = account.row
            account.last_direction = account.direction
            account.actions = ''
            account.save()

        print 'Action hash setup complete.'

        for second in range(10):
            for account in Account.objects.all():
                this_action_name = all_actions[account.id][second]
                if this_action_name != 'walk-start' and this_action_name != 'noop':

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

                    if account.col < 1: account.col = 1
                    if account.col > 48: account.col = 48
                    if account.row < 1: account.row = 1
                    if account.row > 73: account.row = 73
                    account.save()


                if account.col not in player_locations:
                    player_locations[account.col] = {}
                
                if account.row not in player_locations[account.col]:
                    player_locations[account.col][account.row] = []

                if account not in player_locations[account.col][account.row]:
                    player_locations[account.col][account.row].append(account)

        print 'Action resolutions finished'

        for row in range(75):
            for col in range(50):
                if player_locations.has_key(col):
                    if player_locations[col].has_key(row):
                        players_in_this_square = player_locations[col][row]
                        if len(players_in_this_square) >= 2:
                            seen = {}
                            for account in players_in_this_square:
                                for other_account in players_in_this_square:
                                    if account != other_account and (not seen.has_key(str(account.id) + '|' + str(other_account.id))) and (not seen.has_key(str(other_account.id) + '|' + str(account.id))):
                                        if account.team != other_account.team:
                                            if col < 25:
                                                if account.team == 'blue':
                                                    account.col = BLUE_START['col']
                                                    account.row = BLUE_START['row']
                                                    other_account.enemies_tagged += 1
                                                if other_account.team == 'blue':
                                                    other_account.col = BLUE_START['col']
                                                    other_account.row = BLUE_START['row']
                                                    account.enemies_tagged += 1
                                            else:
                                                if account.team == 'red':
                                                    account.col = RED_START['col']
                                                    account.row = RED_START['row']
                                                    other_account.enemies_tagged += 1
                                                if other_account.team == 'red':
                                                    other_account.col = RED_START['col']
                                                    other_account.row = RED_START['row']
                                                    account.enemies_tagged += 1
                                            account.save()
                                            other_account.save()
                                            seen[str(account.id) + '|' + str(other_account.id)] = True
                                            seen[str(other_account.id) + '|' + str(account.id)] = True



        squares = Square.objects.order_by('row', 'col')

        im = Image.new('RGB', (50, 75), 'black')

        for square in squares:
            terrain = square.get_terrain_type()
            if terrain == 'grass':
                color = (102, 188, 83)
            elif terrain == 'water':
                color = (71, 132, 224)
            elif terrain == 'corn':
                color = (255, 255, 0)
            elif terrain == 'rock':
                color = (160, 160, 160)
            elif terrain == 'trees':
                color = (8, 74, 41)
            elif terrain == 'dirt':
                color = (205, 115, 32)
            elif terrain == 'shrubbery':
                color = (8, 74, 41)
            elif terrain == 'road':
                color = (200, 200, 200)
            elif terrain == 'red-flag':
                color = (150, 0, 30)
            elif terrain == 'blue-flag':
                color = (0, 0, 196)

            if terrain == 'red-flag' or terrain == 'blue-flag':
                im.putpixel((square.col, square.row), color)
                im.putpixel((square.col-1, square.row), color)
                im.putpixel((square.col-1, square.row-1), color)
                im.putpixel((square.col-1, square.row+1), color)

                im.putpixel((square.col+1, square.row), color)
            else:
                im.putpixel((square.col, square.row), color)

        for account in Account.objects.filter(inactive_turns__lt=settings.TURNS_TILL_DEACTIVATION):
            if account.team == 'red':
                color = (255, 0, 0)
            elif terrain == 'blue':
                color = (0, 0, 255)

            im.putpixel((account.col, account.row), color)
            im.putpixel((account.col-1, account.row), color)
            im.putpixel((account.col+1, account.row), color)
            im.putpixel((account.col, account.row-1), color)
            im.putpixel((account.col, account.row+1), color)
           
        im = im.resize((250, 375), Image.NEAREST)

        im.save('static/images/minimap.png', 'PNG')
