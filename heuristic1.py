# -*- coding: utf-8 -*-
#import search
import numpy as np
from copy import deepcopy as dc
import math

def heuristic1(b):
    score = 0
    mx = 0
    numtiles = 0
    corner = 0
    for row in b.board:
        for tile in row:
            if tile > mx:
                mx = tile
            if tile != 0:
                numtiles+=1
                score += math.log(tile,2)
    corner += b.board[0][0] + b.board[0][3] + b.board[3][0] + b.board[3][3]
    total = corner + mx - numtiles + score
    return total

