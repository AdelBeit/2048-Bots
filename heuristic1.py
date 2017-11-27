# -*- coding: utf-8 -*-
#import search
import numpy as np
from copy import deepcopy as dc
import math

def heuristic1(b,a):
    logs = 0
    biggestnum = 0
    numtiles = 0
    corners = 0
    total = 0
    openSpots_total = 0
    rowLikeness_total = 0
    columnLikeness_total = 0
    maxOnCorner = 0
    board = b.board
    
    # biggestnum : find the biggest number in board
    # numtiles : find the board with least number of tiles
    # logs : find the logs of all non zero tiles in state
    for row in board:
        for tile in row:
            if tile > biggestnum:
                biggestnum = tile
            if tile != 0:
                numtiles-=1
                logs += math.log(tile,2)

    # get the sum of logs of nums on corners
    corners += math.log(b.board[0][0]+2,2) + math.log(b.board[0][3]+2,2) + math.log(b.board[3][0]+2,2) + math.log(b.board[3][3]+2,2)

    #find states with most mergable tiles
    mergescore = 0
    cols = np.array(b.board).tolist()
    rows = b.board
    mergescore += findmergers(cols)
    mergescore += findmergers(rows)
    
    #score total number of open spaces
    for x in range(4):
        for y in range(4):
            if(board[x][y] == 0):
                openSpots_total += 10
    openSpots_total *= 1
    
    #score matching tiles in rows
    for x in range(4):
        for y in range(3):
            if(board[x][y] != 0):
                if(board[x][y] == board[x][y+1]):
                    rowLikeness_total += 10
    rowLikeness_total *= 1
    
    #score matching tiles in columns
    for x in range(4):
        for y in range(3):
            if(board[y][x] != 0):
                if(board[y][x] == board[y+1][x]):
                    columnLikeness_total += 10
    columnLikeness_total *= 1
    
    #bonus for max value being on edge/corner
    mx = max([max(i) for i in board])
    for x in range(4):
        for y in range(4):
            if(board[x][y] == mx):
                if((x == 0 and (y == 0 or y == 3)) or
                    (x == 3 and (y == 0 or y == 3))):
                    maxOnCorner += mx
                elif(x == 0 or x == 3 or y == 0 or y == 3):
                    maxOnCorner += mx*.5

    if a[0]:
        total += corners
    if a[1]:
        total += biggestnum
    if a[2]:
        total += numtiles
    if a[3]:
        total += logs
    if a[4]:
        total += mergescore
    if a[5]:
        total += openSpots_total
    if a[6]:
        total += rowLikeness_total
    if a[7]:
        total += columnLikeness_total
    if a[8]:
        total += maxOnCorner
        
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


def oo():
    board = [[0,0,1,50],[0,1,2,0],[9,100,0,0],[0,0,0,0]]
    mx = max(board[0])
    for x in range(1, 4):
        tmp = max(board[x])
        if(tmp > mx):
            mx = tmp
    print(mx)
    ll = max([max(i) for i in board])
    print(ll)
