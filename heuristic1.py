# -*- coding: utf-8 -*-
#import search
import numpy as np
from copy import deepcopy as dc
import math

def heuristic1(b):
    logs = 0
    biggestnum = 0
    numtiles = 0
    corners = 0
    for row in b.board:
        for tile in row:
            if tile > biggestnum:
                biggestnum = tile
            if tile != 0:
                numtiles-=1
                logs += math.log(tile,2)
    corners += math.log(b.board[0][0]+2,2) + math.log(b.board[0][3]+2,2) + math.log(b.board[3][0]+2,2) + math.log(b.board[3][3]+2,2)
    total = corners + biggestnum + numtiles + logs

    #find moves that merge the most
    mergescore = 0
    cols = np.array(b.board).tolist()
    rows = b.board
    mergescore += findmergers(cols)
    mergescore += findmergers(rows)
    total += mergescore
    return total

def findmergers(b):
    prevnum = 0
    score = 0
    for row in b:
        prenum = row[0]
        for i in row:
            if i != 0:
                if i == prevnum:
                    score += 1
                if i != prevnum:
                    prevnum = i
                    score -= 1
    return score
    
        
