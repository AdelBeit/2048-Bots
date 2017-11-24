from copy import deepcopy 
import random
import ai_helper as aihelper
import ai_opponent as aiantagonist

class Board():
        
    def __init__(self):
        self.board = [[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]
        self.shifts_made = list()
        self.tiles_placed = list()
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
        moves = list()
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                if(self.board[x][y] == 0):
                    moves.append(((x, y), 2))
                    moves.append(((x, y), 4))
        return moves

    def previewMove(self, move):
        copy_of_self = deepcopy(self)
        
        if(copy_of_self.shifters_turn): #shift tiles
            copy_of_self.makeMoves_ShiftTiles(move)
        else: #place tiles
            copy_of_self.makeMoves_PlaceTiles(move)
        copy_of_self.shifters_turn = not(copy_of_self.shifters_turn)
        return copy_of_self
    
    def makeMoves(self, move):
        if(self.shifters_turn): #shift tiles
            self.makeMoves_ShiftTiles(move)
        else: #place tiles
            self.makeMoves_PlaceTiles(move)
        self.shifters_turn = not(self.shifters_turn)
    
    def makeMoves_ShiftTiles(self, direction):
        
        self.previous_board_state = deepcopy(self.board)
        self.shifts_made.append(direction)
        
        if(direction == "up"):
            self.board = self.shift_up()
        elif(direction == "down"):
            self.board = self.shift_down()
        elif(direction == "left"):
            self.board = self.shift_left()
        elif(direction == "right"):
            self.board = self.shift_right() 
        else:
            print("error, wrong argument: %s" % direction)
    
    def shift_up(self):
        #print("SHIFTING UP")
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
                            #print("merging at column %d" % x)
                            board[top_most_open - 1][x] = board[top_most_open - 1][x]*2
                            board[top_most_open][x] = 0
                            zero_spaces.insert(0, top_most_open)
                elif(y > 0 and board[y-1][x] == board[y][x]):
                    #print("merging at column %d" % x)
                    board[y-1][x] = board[y-1][x]*2
                    board[y][x] = 0
                    zero_spaces.insert(0, y)
            zero_spaces.clear()
        return board
    
    def shift_down(self):
        #print("SHIFTING DOWN")
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
                            #print("merging at column %d" % x)
                            board[bottom_most_open + 1][x] = board[bottom_most_open + 1][x]*2
                            board[bottom_most_open][x] = 0
                            zero_spaces.insert(0, bottom_most_open)
                elif(y < 3 and board[y + 1][x] == board[y][x]):
                    #print("merging at column %d" % x)
                    board[y + 1][x] = board[y + 1][x]*2
                    board[y][x] = 0
                    zero_spaces.insert(0, y)
            zero_spaces.clear()
        return board
    
    def shift_left(self):
        #print("SHIFTING LEFT")
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
                            #print("merging at row %d" % x)
                            board[x][left_most_open - 1] = board[x][left_most_open - 1]*2
                            board[x][left_most_open] = 0
                            zero_spaces.insert(0, left_most_open)
                elif(y > 0 and board[x][y - 1] == board[x][y]):
                    #print("merging at row %d" % x)
                    board[x][y - 1] = board[x][y - 1]*2
                    board[x][y] = 0
                    zero_spaces.insert(0, y)
            zero_spaces.clear()
        return board
    
    def shift_right(self):
        #print("SHIFT RIGHT")
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
                            #print("merging at row %d" % x)
                            board[x][right_most_open + 1] = board[x][right_most_open + 1]*2
                            board[x][right_most_open] = 0
                            zero_spaces.insert(0, right_most_open)
                elif(y < 3 and board[x][y + 1] == board[x][y]):
                    #print("merging at row %d" % x)
                    board[x][y + 1] = board[x][y + 1]*2
                    board[x][y] = 0
                    zero_spaces.insert(0, y)
            zero_spaces.clear()
        return board
    
    def makeMoves_PlaceTiles(self, move):
        self.previous_board_state = deepcopy(self.board)
        
        if(not self.tiles_placed): #first move of the game is random and selects 2 tile placements
            moves = self.generateMoves()
            move1 = random.choice(moves)
            moves.remove(move1)
            move2 = random.choice(moves)
            self.board[move1[0][0]][move1[0][1]] = move1[1]
            self.board[move2[0][0]][move2[0][1]] = move2[1]
        else:
            self.board[move[0][0]][move[0][1]] = move[1]
            
        self.tiles_placed.append(move)
     
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
            return (self.previous_board_state != None) and (not self.generateMoves_ShiftTiles())
    
    def aiWon(self):
        for x in range(4):
            for y in range(4):
                if(self.board[x][y] == 2048):
                    return True   
        return False
    
def main():
    b1 = Board()
    ai_good = aihelper.AIHelper(b1)
    ai_bad = aiantagonist.Antagonist(b1)
    iterations = 0
    while(not b1.gameOver()):
        moves = b1.generateMoves()
        print(iterations)
        if(b1.shifters_turn):
            bestMove = ai_good.alpha_beta(b1, 1)
            b1.makeMoves(bestMove)
        else:
            #bestMove = ai_bad.alpha_beta(b1, 1)
            #b1.makeMoves(bestMove)
            b1.makeMoves(random.choice(moves))
        print(b1)
        iterations += 1

if __name__=="__main__":
    main()
