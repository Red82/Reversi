# -*- coding: utf-8 -*-
import operator
from pprint import pprint

#Reversi playing AI
class Board:
    def __init__(self):
        pass

    #Matrix brute force
    def moves(self, state, player, enemy):
        weights = {}

        for y in xrange(len(state)):
            for x in xrange(len(state[0])):
                
                weights[(x, y)] = self.calc_move(x, y, state, player, enemy)
                #pprint({(x, y) : weights[(x, y)]})
                
        sorted_dict = sorted(weights.iteritems(), key=operator.itemgetter(1))
        
        return sorted_dict[-1][0]         

    #Calculation of the weighting factor for each direction
    def calc_move(self, x, y, state, player, enemy):
        if state[y][x] != 0:
            return False


        weight = 0
        for direction in ((-1, -1), (0, -1), (1, -1),
                            (-1, 0), (1, 0),
                            (-1, 1), (0, 1), (1, 1)):

            weight += self.slice_direction(direction, state, x, y, player, enemy)
            
        return weight

    #The number of chips the enemy
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
        return False
