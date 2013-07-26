# -*- coding: utf-8 -*-

import os, sys
import json
import urllib2
from copy import deepcopy
from pprint import pprint 

#API
class Reversi:
    def __init__(self, ):
        pass
    
    #Create HTTP Request, get Response.
    def send_req(self, request):
        print request
        req = urllib2.Request('http://reversi.laszlo.nu:1337' + request)
        res = urllib2.urlopen(req).read()
        data = json.loads(res)
        return data
    
    #Will return {"key": <api key>} on success.
    def register(self, mail):
        data = self.send_req('/register/' + mail)
        return str(data)

    #Will return all your active games
    def list_games(self, key):
        data = self.send_req('/listgames/' + key)
        return data
    
    #Like listgames, but will also returned finished games
    def list_all_games(self, key):
        data = self.send_req('/listallgames/' + key)
        return data
    
    #Will return your score:
    def score(self, key):
        data = self.send_req('/score/' + key)
        return data        

    #Create new game
    def new_game(self, key):
        data = self.send_req('/newgame/' + key)
        return data

    #The state of game
    def state_game(self, key,game_id):
        data = self.send_req('/state/' + key + '/' + game_id)
        return data

    #Move checer
    def move(self, key, game_id, x, y):
        data = self.send_req('/move/' + key + '/' + game_id + '/' + x + ',' + y)
        return data

    #Check register your e-mail
    def mail_check(self, mail):
        err = str({u'error': u"Couldn't register. Email already exists?"})
        if self.register(mail) == err:
            return True
        else:
            return False

    #Color's definer
    def color_definer(self, key):
        res = self.new_game(key)
        return res['server_color']

    #
    def play(self, key, res):
        #x = raw_input('Please, enter x = ')
        #y = raw_input('Please, enter y = ')
        if res['server_color'] == 1:
            player = 2
        else:
            player = 1
        d_board = Board(res['board'])
        d_board.moves(player)
        x = '6'
        y = '2'
        res = self.move(key, res['id'], x, y)
        return res

    #Show board
    def display(self, res): 
        pprint(res)

#Reversi playing AI
class Board:
    def __init__(self, initial_state):
        self.internal_state = deepcopy(initial_state)

    #Move checer
    def move(self, x, y, player):
        new_state = Board(self.internal_state)
        new_state.internal_state[x][y] = player
        return new_state

    #Matrix brute force
    def moves(self, player):
        for i in xrange(len(self.internal_state) - 1):
            for j in xrange(len(len(self.internal_state[0])) - 1):
                if self.is_move_acceptable(i, j, player):
                    yield self.move(i, j, player)

    #Сheck matrix cells
    def is_move_acceptable(self, x, y, player):
        if self.internal_state[x][y] != 0:
            return False

        result = False

        for direction in ((-1, -1), (0, -1), (1, -1),
                          (-1, 0), (1, 0),
                          (-1, 1), (0, 1), (1, 1)):

            slice = self.slice_direction(direction, x, y)

            if self.is_valid_pattern(slice, player):
                return True                 

        return result

       # TODO: should generate the list of all cells values from the current point to the board side (like a slice)
    def slice_direction(self, direction, x, y):

        cursor = [x, y]
        line = []

        while 0 <= cursor[0] < len(len(self.internal_state[0]-1)) and
                0 <= cursor[1] < len(self.internal_state[1]-1):

            cursor[0] += direction[0]
            cursor[1] += direction[1]
            line.append(self.internal_state[[cursor[0]], [cursor[1]]])
        
        
        # cursor = [x, y]
        #
        # line = []
        #
        # while 0 <= cursor[0] < len(len(self.internal_state[0])) and 0 <= cursor[1] < len(self.internal_state[1]):
        #     cursor[0] += direction[0]
        #     cursor[1] += direction[1]
        #     line.append(self.internal_state[[cursor[0], cursor[1]]])
    
        pass

    # Validates the direction slice for potential revert presence.
    # TODO: can be implemented using simple Finite State Machine (you can use just a regex) or just ad-hoc
    def is_valid_pattern(self, slice, player):

        print('is_valid_pattern not implemented yet')
        return True    

   #Show board
    def print_self(self):
        pprint(self.internal_state)
        
    
def main():
    confirm = 1
    key = u'c459b21f8cdd0ddfc49b3dda90eb1b64b676d9dc'
    r = Reversi()
    
    if r.mail_check('appp_red@mail.ru'):
        res = r.new_game(key)
        
        while res['state'] == "playing":
            r.display(res)
            
            if confirm:
                raw_input('Press enter to continue...')
            res = r.play(key, res)
            pprint(res)
            
        pprint(r.score(key))
            

      
    #print r.send_req('/register/appp_red@mail.ru')
    #print r.list_games('c459b21f8cdd0ddfc49b3dda90eb1b64b676d9dc')
    #print r.list_all_games('c459b21f8cdd0ddfc49b3dda90eb1b64b676d9dc')
    #print r.new_game('c459b21f8cdd0ddfc49b3dda90eb1b64b676d9dc')

if __name__ == '__main__':
    main()
    
