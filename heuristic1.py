# -*- coding: utf-8 -*-
#import search
import numpy as np
from copy import deepcopy as dc

def heuristic1(board):
    score = 0
    mx = 0
    numtiles = 0
    for row in board:
        for tile in row:
            if tile > mx:
                mx = tile
            if tile != 0:
                numtiles+=1
                score += math.log(tile,2)
    return (score,mx,numtiles)
