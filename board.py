# -*- coding: utf-8 -*-
#import search
import numpy as np
from copy import deepcopy as dc
class Board:
    emptyspot = 0
    width = 4
    height = 4
    maxplayer = "Mover"
    minplayer = "Placer"
    
    def __init__(self,parent=None):
        self.turn = self.maxplayer
        self.board = self.clean_board()
        self.parent = parent
        self.won = False

    def set_parent(self,parent):
        self.parent = parent

    def set_board(self,board):
        self.board = board

    # checks if given list has empty room
    def has_empty(self,lst):
        return emptyspot in lst

    # merge in the given direction if possible
    def merge(self,b=None,d):
        # preprocess the lists so they can be iterated over in a single for loop
        # reverse cols for processing if u can move in that way
        if d == 'u':
            b = reverse_matrix_rows(self.get_cols(b))
        if d == 'l':
            b = reverse_matrix_rows(self.board)
        if d == 'd':
            b = self.get_cols(b)
        if d == 'r':
            b = self.board
        mergable = False
        r = 0
        # go through the tiles rows and check for combos
        while tcount < self.width-1:
            m = can_merge(b[r])
            if can_merge(b)[1]:

    # checks if a list has tiles that are mergable and returns mergable spots
    def can_merge(self,l):
        c = 0
        mergables = []
        mergable = False
        while c < len(l):
            if l[c] == l[c+1]:
                mergables.append(c)
                mergable = True
            c+=2
        return (mergables,mergable)
            
    def reverse_matrix_rows(self,b):
        b = dc(b)
        for i in range(len(b)):
            b[i] = b[i][::-1]
        return b
    
    def get_cols(self,b):
        if b == None:
            b = self.board
        # get arr rep of board
        barr = np.array(b)
        barr = barr.transpose()
        cols = barr.tolist()
        return cols
    
    def get_left_col(self,b=None):
        return self.get_cols(b)[0]

    def get_right_col(self,b=None):
        return self.get_cols(b)[self.width-1]

    def get_top_row(self,b=None):
        if b==None:
            b = self.board
        return b[0]

    def get_bottom_row(self,b=None):
        if b==None:
            b = self.board
        return b[height-1]
        
    def generate_moves(self):
        moves = []
        top = self.get_top_row()
        bot = self.get_bottom_row()
        left = self.get_left_col()
        right = self.get_right_col()
        # clockwise t-l
        options = [top,right,bottom,left]
        counter = 0
        while counter < 4:
            for l in options[counter]:
                if self.emptyspot in l:
                    moves.append(counter)
            counter += 1
        
        moves = []
        for col in range(self.width):
            if self.board[0][col] == self.emptyspot:
                moves.append(col)
        return moves

    # returns a new board with the move
    def make_move(self,c):
        if self.board[0][c] == self.emptyspot:
            p = dc(self.board)
            b = dc(self)
            for row in range(self.height-1, -1, -1):
                if self.board[row][c] == self.emptyspot:
                    self.board[row][c] = self.turn
                    parent = Board(p)
                    parent.set_board(p)
                    parent.set_parent(self.parent)
                    self.set_parent(parent)
                    self.switch_turns()
                    return self
        return None
        
    def unmake_last_move(self):
        if self.parent != None:
            p = self.parent
            self.set_board(p.board)
            self.set_parent(p.parent)
            self.switch_turns()
                
    def last_move_won(self):
        # get arr rep of board
        barr = np.array(self.board)
        barr = barr.transpose()
        # make a list of lists that contains diag, hor, and ver rows
        backslashdiag = []
        forwardslashdiag = []
        vertical = barr.tolist()
        horizontal = self.board
        flipboard = np.flipud(self.board)
        rows = [vertical,horizontal,backslashdiag,forwardslashdiag]
        p = self.opposite_player()
        
        for i in range(-(self.height-1), self.width):
            # \ back slash
            backslashdiag.append(np.diag(self.board,k=i).tolist())
            # / forward slash
            forwardslashdiag.append(np.diag(flipboard,k=i).tolist())
        
        # check boards for winning cond
        for board in rows:
            if self.same4(board,p):
                self.won = True
                self.game_over()
                return self.won
        
        return False
    
    # prs board and ends game
    def game_over(self):
        p = self.opposite_player()

    def __str__(self):
        return str(np.matrix(self.board))

    # returns an empty board template
    def clean_board(self):
        b = []
        for row in range(self.height):
            b.append([])
            for col in range(self.width):
                b[row].append(self.emptyspot)
        return b

    # switch player turns
    def switch_turns(self):
        self.turn = self.opposite_player(self.turn)

    # returns the opposite player
    def opposite_player(self,p=None):
        p = self.turn if p == None else p
        return self.minplayer if p == self.maxplayer else self.maxplayer
