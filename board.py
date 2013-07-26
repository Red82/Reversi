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

        for y in xrange(len(state)-1):
            for x in xrange(len(state[0]) - 1):
                
                weights[(x, y)] = self.calc_move(x, y, state, player, enemy)
                pprint({(x, y) : weights[(x, y)]})
                
        sorted_dict = sorted(weights.iteritems(), key=operator.itemgetter(1))

        if sorted_dict[-1][1] == 0:
            return 
        
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
