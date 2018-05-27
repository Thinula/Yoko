import BitBoard
import numpy as np

def oppCol(col):
    return "W" if col == "B" else "B"

class Transpose:

    def __init__(self,score,depth):
        self.score = score
        self.depth = depth
    def getScore(self):
        return self.score
    def getDepth(self):
        return self.depth

INT_MAX = 10000000000000000    
class AI:

    def __init__(self):
        self.maxDepth = 6
        self.posTranspose = {}
        # weights and threshold used in Neural Network
        #self.inputWeights = weights1
        #self.hiddenWeights = weights2
        #self.threshold = threshold
        # Neural Network has input/hidden layer -> |hidden| ~ 2/3*|input|
        #self.layer1 = np.zeros((64,1)) # 64 by 1 array of 0s
        #self.layer2 = np.zeros((42,1)) # 42 by 1 array of 0s

    def evaluate(self,board,playerCol):
        playerDiscs = board.getDiscs(playerCol)
        oppDiscs = board.getDiscs(oppCol(playerCol))

        count = 0
        while playerDiscs != 0:
            playerDiscs &= (playerDiscs-1)
            count += 1
        while oppDiscs != 0:
            oppDiscs &= (oppDiscs-1)
            count -= 1
        return count

    def makeMove(self,board,playerCol):

         moves = board.getAllValidMoves(playerCol)
         playerMoves = board.getAllValidMoves(playerCol)
         oppMoves = board.getAllValidMoves(oppCol(playerCol))
         bestScore = -INT_MAX
         bestMove = -1
         #self.posTranspose = {}
         for i in range(64):
             if (playerMoves & (1 << i)) == 0:
                continue

             tempBoard = BitBoard.BitBoard(board)
             tempBoard.makeMove(playerCol,i)

             score = self.alphaBeta(tempBoard,playerCol,0,-INT_MAX,INT_MAX,False)  
             #score = self.negaMax(tempBoard,playerCol,0,-INT_MAX,INT_MAX)
             if score > bestScore:
                 bestScore = score
                 bestMove = i
         return bestMove

    def alphaBeta(self,board,col,depth,alpha,beta,maximizingPlayer):

        playerMoves = board.getAllValidMoves(col)
        oppMoves = board.getAllValidMoves(oppCol(col))

        if playerMoves == 0 or depth == self.maxDepth:
            return self.evaluate(board,col)
        
        if maximizingPlayer:
            v = -INT_MAX
            for i in range(64):
                if (playerMoves & (1 << i)) == 0:
                    continue
                tempBoard = BitBoard.BitBoard(board)
                tempBoard.makeMove(col,i)
                trans = self.posTranspose.get(tempBoard)

                if trans is None or depth <= trans.getDepth():
                    v = max(v,self.alphaBeta(tempBoard,oppCol(col),depth+1,alpha,beta,False))
                    self.posTranspose[tempBoard] = Transpose(v,depth)
                else:
                    v = trans.getScore()

                alpha = max(alpha,v)
                if beta <= alpha:
                    break
            return v

        else:
            v = INT_MAX
            for i in range(64):
                if (playerMoves & (1 << i)) == 0:
                    continue
                tempBoard = BitBoard.BitBoard(board)
                tempBoard.makeMove(col,i)
                trans = self.posTranspose.get(tempBoard)

                if trans is None or depth <= trans.getDepth():
                    v = min(v,self.alphaBeta(tempBoard,oppCol(col),depth+1,alpha,beta,True))
                    self.posTranspose[tempBoard] = Transpose(v,depth)
                else:
                    v = trans.getScore()

                beta = min(beta,v)
                if beta <= alpha:
                    break
            return v
                    
        
    def negaMax(self,board,playerCol,depth,alpha,beta):
        
        playerMoves = board.getAllValidMoves(playerCol)
        oppMoves = board.getAllValidMoves(oppCol(playerCol))

        # must pass then
        if playerMoves == 0 and oppMoves != 0:
            return -self.negaMax(board,oppCol(playerCol),depth,-beta,-alpha)
        # reached end of search 
        elif depth == self.maxDepth or (playerMoves == 0 and oppMoves == 0):
            return self.evaluate(board,playerCol)

        best = -INT_MAX
        for i in range(64):
            if (playerMoves & (1 << i)) == 0:
                continue

            tempBoard = BitBoard.BitBoard(board)
            tempBoard.makeMove(playerCol,i)
            trans = self.posTranspose.get(tempBoard)
            
            if trans is None or depth <= trans.getDepth():
                best = max(best,-self.negaMax(tempBoard,oppCol(playerCol),depth+1,-beta,-alpha))
                self.posTranspose[tempBoard] = Transpose(best,depth)
            else:
                best = trans.getScore()
                    
            alpha = max(best,alpha)
            if beta <= alpha:
                break

        return best
        
            






                





















        
