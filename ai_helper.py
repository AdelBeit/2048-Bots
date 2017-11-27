import heuristic1 as h1

class AIHelper:
    
    def __init__(self, b, a=[0,0,0,0,0,0,0,0,0]):
        self.board = b
        self.name = "2048 Bot"
        self.a = a
        
    def makeMove(self, move):
        self.board.makeMoves(move)
    
    def getMoves(self):
        move = self.alpha_beta(self.board, 2)
        return move
        
    def alpha_beta(self ,b, depth):
        moves = b.generateMoves()
        bestMove = -1
        bestValue = float("-inf")
        p_inf = float("inf")
        n_inf = float("-inf")
        for x in moves:
            nextBoardState = b.previewMove(x)
            score = self.min_value_ab(nextBoardState, depth-1, p_inf, n_inf)
            if(score > bestValue):
                bestMove = x
                bestValue = score
        #print("Best Value %d : Best Move %s" % (bestValue, bestMove))
        return bestMove
        
    def max_value_ab(self, b, depth, alpha, beta):
        if(depth == 0 or b.gameOver()):
            return self.evaluation(b)
        moves = b.generateMoves()
        bestValue = float("-inf")
        for x in moves:
            nextBoardState = b.previewMove(x)
            bestValue = max(bestValue, self.min_value_ab(nextBoardState, depth-1, alpha, beta))
            if(bestValue >= beta):
                return bestValue
            alpha = max(alpha, bestValue)
        return bestValue

    def min_value_ab(self, b, depth, alpha, beta):
        if(depth == 0 or b.gameOver()):
            return self.evaluation(b)
        moves = b.generateMoves()
        bestValue = float("inf")
        for x in moves:
            nextBoardState = b.previewMove(x)
            bestValue = min(bestValue, self.max_value_ab(nextBoardState, depth-1, alpha, beta))
            if(bestValue <= alpha):
                return bestValue
            beta = min(beta, bestValue)
        return bestValue
    

    def evaluation_v2(self, b):
        total = h1.heuristic1(b,self.a)
		return total
		
    def evaluation(self, b):
        board = b.board
        total = 0
        openSpots_total = 0
        rowLikeness_total = 0
        columnLikeness_total = 0
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
        mx = max(board[0])
        for x in range(1, 4):
            tmp = max(board[x])
            if(tmp > mx):
                mx = tmp
        for x in range(4):
            for y in range(4):
                if(board[x][y] == mx):
                    if((x == 0 and (y == 0 or y == 3)) or
                       (x == 3 and (y == 0 or y == 3))):
                        total += mx
                    elif(x == 0 or x == 3 or y == 0 or y == 3):
                        total += mx*.5

        total = openSpots_total + rowLikeness_total + columnLikeness_total
        return total
        
