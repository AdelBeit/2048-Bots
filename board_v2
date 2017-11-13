from copy import deepcopy 
import random

class Board():
        
    def __init__(self):
        self.board = [[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]
        self.movesMade = list()
        self.shifters_turn = False
        self.previous_board_state = None
        
    def __str__(self):
        output = ""
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                chars = len(str(self.board[x][y]))
                if(chars == 4):
                    output += " " + str(self.board[x][y])
                elif(chars == 3):
                    output += " " + str(self.board[x][y]) + " "
                elif(chars == 2):
                    output += "  " + str(self.board[x][y]) + "  "
                else: 
                    output += "   " + str(self.board[x][y]) + "  "
            output += "\n"
        
        return output
        
    def generateMoves(self):
        if(self.shifters_turn):
            return self.generateMoves_ShiftTiles()
        else:
            return self.generateMoves_PlaceTiles()
        
    def generateMoves_ShiftTiles(self):
        moves = list()
        terminate = False
        #right shift available
        for x in range(len(self.board)):
            if(terminate):
                break
            for y in range(len(self.board[x]) - 1): 
                if(self.board[x][y] != 0):
                    if(self.board[x][y+1] == 0 or self.board[x][y+1] == self.board[x][y]):
                        moves.append("right")
                        terminate = True
                        break
        #left shift available
        terminate = False
        for x in range(len(self.board)):
            if(terminate):
                break
            for y in range(len(self.board[x]) - 1, 0, -1):
                if(self.board[x][y] != 0):
                    if(self.board[x][y-1] == 0 or self.board[x][y-1] == self.board[x][y]):
                        moves.append("left")
                        terminate = True
                        break
        #down shift available
        terminate = False
        for x in range(len(self.board) - 1):
            if(terminate):
                break
            for y in range(len(self.board[x])):
                if(self.board[x][y] != 0):
                    if(self.board[x+1][y] == 0 or self.board[x+1][y] == self.board[x][y]):
                        moves.append("down")
                        terminate = True
                        break
        #up shift available
        terminate = False
        for x in range(len(self.board) - 1, 0, -1):
            if(terminate):
                break
            for y in range(len(self.board[x])):
                if(self.board[x][y] != 0):
                    if(self.board[x-1][y] == 0 or self.board[x-1][y] == self.board[x][y]):
                        moves.append("up")
                        terminate = True
                        break
        return moves
        
    def generateMoves_PlaceTiles(self):
        openSpaces = list()
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                if(self.board[x][y] == 0):
                    openSpaces.append((x, y))
        #append all possible combinations of 2 selected tiles and values to moves
        moves = list()
        if(len(openSpaces) > 1): #more than 1 spot is open on the board
            seen = list()
            copy = openSpaces.copy()
            for x in openSpaces:
                for y in copy:
                    if(y != x and y not in seen):
                        tuple1 = (x, 2)
                        tuple2 = (y, 2)
                        combined = (tuple1, tuple2)
                        moves.append(combined)
                        
                        tuple1 = (x, 2)
                        tuple2 = (y, 4)
                        combined = (tuple1, tuple2)
                        moves.append(combined)
                        
                        tuple1 = (x, 4)
                        tuple2 = (y, 2)
                        combined = (tuple1, tuple2)
                        moves.append(combined)
                        
                        tuple1 = (x, 4)
                        tuple2 = (y, 4)
                        combined = (tuple1, tuple2)
                        moves.append(combined) 
                seen.append(x)
                
        elif(len(openSpaces) == 1): #1 spot is open on the board
            tuple1 = (openSpaces[0], 2)
            tuple2 = (openSpaces[0], 4)
            moves.append((tuple1, None))
            moves.append((tuple2, None))
        else:
            moves.append((None, None))
            print("No available spaces to place new tiles: if there are no available shifts: gameover")
        return moves
            
    
    def makeMoves(self, move):
        if(self.shifters_turn): #shift tiles
            self.makeMoves_ShiftTiles(move)
        else: #place tiles
            self.makeMoves_PlaceTiles(move)
        self.shifters_turn = not(self.shifters_turn)
    
    def makeMoves_ShiftTiles(self, direction):
        if(direction == "up"):
            self.previous_board_state = deepcopy(self.board)
            self.board = self.shift_up()
        elif(direction == "down"):
            self.previous_board_state = deepcopy(self.board)
            self.board = self.shift_down()
        elif(direction == "left"):
            self.previous_board_state = deepcopy(self.board)
            self.board = self.shift_left()
        elif(direction == "right"):
            self.previous_board_state = deepcopy(self.board)
            self.board = self.shift_right() 
        else:
            print("error, wrong argument: %s" % direction)
    
    def shift_up(self):
        print("SHIFTING UP")
        board = deepcopy(self.board)
        zero_spaces = list()
        #shift and merge up
        for x in range(4):
            for y in range(4):
                if(board[y][x] == 0):
                    zero_spaces.append(y)
                elif(zero_spaces):
                    top_most_open = zero_spaces.pop(0)
                    board[top_most_open][x] = board[y][x]
                    board[y][x] = 0
                    zero_spaces.append(y)
                    if(top_most_open > 0):
                        if(board[top_most_open][x] == board[top_most_open - 1][x]):
                            print("merging at column %d" % x)
                            board[top_most_open - 1][x] = board[top_most_open - 1][x]*2
                            board[top_most_open][x] = 0
                            zero_spaces.insert(0, top_most_open)
                elif(y > 0 and board[y-1][x] == board[y][x]):
                    print("merging at column %d" % x)
                    board[y-1][x] = board[y-1][x]*2
                    board[y][x] = 0
                    zero_spaces.insert(0, y)
            zero_spaces.clear()
        return board
    
    def shift_down(self):
        print("SHIFTING DOWN")
        board = deepcopy(self.board)
        zero_spaces = list()
        #shift and merge down
        for x in range(4):
            for y in range(3, -1, -1):
                if(board[y][x] == 0):
                    zero_spaces.append(y)
                elif(zero_spaces):
                    bottom_most_open = zero_spaces.pop(0)
                    board[bottom_most_open][x] = board[y][x]
                    board[y][x] = 0
                    zero_spaces.append(y)
                    if(bottom_most_open < 3):
                        if(board[bottom_most_open][x] == board[bottom_most_open + 1][x]):
                            print("merging at column %d" % x)
                            board[bottom_most_open + 1][x] = board[bottom_most_open + 1][x]*2
                            board[bottom_most_open][x] = 0
                            zero_spaces.insert(0, bottom_most_open)
                elif(y < 3 and board[y + 1][x] == board[y][x]):
                    print("merging at column %d" % x)
                    board[y + 1][x] = board[y + 1][x]*2
                    board[y][x] = 0
                    zero_spaces.insert(0, y)
            zero_spaces.clear()
        return board
    
    def shift_left(self):
        print("SHIFTING LEFT")
        board = deepcopy(self.board)
        zero_spaces = list()
        #shift and merge left
        for x in range(4):
            for y in range(4):
                if(board[x][y] == 0):
                    zero_spaces.append(y)
                elif(zero_spaces):
                    left_most_open = zero_spaces.pop(0)
                    board[x][left_most_open] = board[x][y]
                    board[x][y] = 0
                    zero_spaces.append(y)
                    if(left_most_open > 0):
                        if(board[x][left_most_open - 1] == board[x][left_most_open]):
                            print("merging at row %d" % x)
                            board[x][left_most_open - 1] = board[x][left_most_open - 1]*2
                            board[x][left_most_open] = 0
                            zero_spaces.insert(0, left_most_open)
                elif(y > 0 and board[x][y - 1] == board[x][y]):
                    print("merging at row %d" % x)
                    board[x][y - 1] = board[x][y - 1]*2
                    board[x][y] = 0
                    zero_spaces.insert(0, y)
            zero_spaces.clear()
        return board
    
    def shift_right(self):
        print("SHIFT RIGHT")
        board = deepcopy(self.board)
        zero_spaces = list()
        #shift and merge right
        for x in range(4):
            for y in range(3, -1, -1):
                if(board[x][y] == 0):
                    zero_spaces.append(y)
                elif(zero_spaces):
                    right_most_open = zero_spaces.pop(0)
                    board[x][right_most_open] = board[x][y]
                    board[x][y] = 0
                    zero_spaces.append(y)
                    if(right_most_open < 3):
                        if(board[x][right_most_open + 1] == board[x][right_most_open]):
                            print("merging at row %d" % x)
                            board[x][right_most_open + 1] = board[x][right_most_open + 1]*2
                            board[x][right_most_open] = 0
                            zero_spaces.insert(0, right_most_open)
                elif(y < 3 and board[x][y + 1] == board[x][y]):
                    print("merging at row %d" % x)
                    board[x][y + 1] = board[x][y + 1]*2
                    board[x][y] = 0
                    zero_spaces.insert(0, y)
            zero_spaces.clear()
        return board
    
    # move is a tuple of tiles where a tile is represented as a set of coordinates and a value
    # move = (((x1, y1), val), ((x2, y2), val))
    def makeMoves_PlaceTiles(self, move):
        if(move[0] == None): # No open spaces, skip turn
            return self.board
        elif(move[1] == None): #only 1 open space
            tuple1 = move[0]
            coord1_value = tuple1[1]
            coord1 = tuple1[0]
            x1 = coord1[0]
            y1 = coord1[1]
            self.board[x1][y1] = coord1_value
        else:
            tuple1 = move[0]
            coord1_value = tuple1[1]
            coord1 = tuple1[0]
            x1 = coord1[0]
            y1 = coord1[1]
            
            tuple2 = move[1]
            coord2_value= tuple2[1]
            coord2 = tuple2[0]
            x2 = coord2[0]
            y2 = coord2[1]
            
            self.board[x1][y1] = coord1_value
            self.board[x2][y2] = coord2_value
        
    def gameOver(self):
        if(self.aiWon()):
            print("AI BOT WINS")
            return True
        elif(self.opponentWon()):
            print("OPPONENT WINS")
            return True
        else:
            return False
            
    
    #checks if there are no available shifts to make
    def opponentWon(self):
        if(self.previous_board_state != None):
            return not self.generateMoves_ShiftTiles()
        else:
            return False
    
    def aiWon(self):
        for x in range(4):
            for y in range(4):
                if(self.board[x][y] == 2048):
                    return True   
        return False
    
def main():
    b1 = Board()
    while(not b1.gameOver()):
        print(b1.shifters_turn)
        moves = b1.generateMoves()
        if(b1.shifters_turn):
            print(moves)
        b1.makeMoves(random.choice(moves))
        print(b1)

if __name__=="__main__":
    main()
