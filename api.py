import os, sys
import json
import urllib2
from copy import deepcopy
from pprint import pprint
from board import Board

#API
class ReversiAPI:
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
