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
        self.board = dc(board)

    # checks if given list has empty room
    def has_empty(self,lst):
        return emptyspot in lst

    # merge and move in the given direction if possible
    def merge_move(self,d,b=None):
        # preprocess the lists so they can be iterated over in a single for loop
        # reverse cols for processing if u can move in that way
        if d == 'u':
            # reverse the cols
            b = self.reverse_matrix_rows(self.get_cols(b))
            # merge
            b = self.merge_helper(b)
            # move
            b = self.move(b)
            # reverse it back
            b = self.reverse_matrix_rows(b)
            # get its cols
            b = self.get_cols(b)
        if d == 'l':
            # reverse the rows
            b = self.reverse_matrix_rows(self.board)
            # merge
            b = self.merge_helper(b)
            # move
            b = self.move(b)
            # reverse it back
            b = self.reverse_matrix_rows(b)
        if d == 'd':
            b = self.get_cols(b)
            # merge 
            b = self.merge_helper(b)
            # move
            b = self.move(b)
            # get its cols
            b = self.get_cols(b)
        if d == 'r':
            b = self.board
            # merge
            b = self.merge_helper(b)
            # move
            b = self.move(b)
        # set main board
        self.set_board(b)
        return b
    
    def merge_helper(self,b):
        r = 0
        # go through the tiles rows and check for combos
        while r < self.width-1:
            m = self.can_merge(b[r])
            if m[1]:
                for l in m[0]:
                    b[r][l] *= 2
                    b[r][l-1] = self.emptyspot
            r+=1
        return b

    # checks if a list has tiles that are mergable and returns mergable spots
    def can_merge(self,l):
        c = 0
        mergables = []
        mergable = False
        k = len(l)
        while c < k:
            if l[c] == l[c+1]:
                mergables.append(c+1)
                mergable = True
                c+=1
                k-=1
            c+=1
        return (mergables,mergable)

    # move the tiles according to direction
    def move(self,b):
        r = 0
        b = self.reverse_matrix_rows(b)
        while r < len(b):
            vals = []
            for i in range(len(b[r])):
                if b[r][i] != self.emptyspot:
                    vals.append(b[r][i])
            vals += [self.emptyspot] * (len(b[r])-len(vals))
            b[r] = vals
            r += 1
        b = self.reverse_matrix_rows(b)
        return b
            
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

def p(s):
    print(str(np.matrix(s)))

def t(k,d):
    i = Board()
    i.set_board(k)
    print('i')
    p(i.board)
    i.merge_move(d)
    print('after',d)
    p(i.board)
    print()

td = [[2,0,8,0],[2,2,4,2],[0,2,2,0],[0,8,2,2]]
lr = [[2,2,0,0],[0,2,2,0],[8,0,2,2],[0,2,8,2]]
t(td,'u')
t(lr,'r')
t(td,'d')
t(lr,'l')
