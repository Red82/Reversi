# -*- coding: utf-8 -*-

import os, sys
import json
import urllib2
from copy import deepcopy
from pprint import pprint
import operator

#API
class Reversi:
    def __init__(self, ):
        self.d_board = Board()
    
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
        data = self.send_req('/move/' + key + '/' + game_id + '/' + str(x) + ',' + str(y))
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
        
        coords = self.d_board.moves(res['board'], res['current_turn'], res['server_color'])
        res = self.move(key, res['id'], coords[0], coords[1])
        return res

    #Show board
    def display(self, res): 
        pprint(res)

#Reversi playing AI
class Board:
    def __init__(self):
        pass

    #Matrix brute force
    def moves(self, state, player, enemy):
        weights = {}
        for y in xrange(len(state)-1):
            for x in xrange(len(state[0]) - 1):
                weights[(x, y)] = self.calc_move(x, y, state, player, enemy)
                pprint({(x, y) : weights[(x, y)]})
        sorted_dict = sorted(weights.iteritems(), key=operator.itemgetter(1))
        return sorted_dict[-1][0]         

    #Сheck matrix cells
    def calc_move(self, x, y, state, player, enemy):
        if state[y][x] != 0:
            return 0


        weight = 0
        for direction in ((-1, -1), (0, -1), (1, -1),
                            (-1, 0), (1, 0),
                            (-1, 1), (0, 1), (1, 1)):

            weight += self.slice_direction(direction, state, x, y, player, enemy)
            
        return weight

       # TODO: should generate the list of all cells values from the current point to the board side (like a slice)
    def slice_direction(self, direction, state, x, y, player, enemy):
        line = []
        x += direction[0]
        y += direction[1]
        while ((0 <= x < len(state[0])) and
                (0 <= y < len(state)) and
                (state[y][x] == enemy)):
            line.append([x, y])
            x += direction[0]
            y += direction[1]
            
        if ((0 <= x < len(state[0])) and
                (0 <= y < len(state)) and
                (state[y][x] == player)):    
            return len(line)
        return 0

    
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
    
