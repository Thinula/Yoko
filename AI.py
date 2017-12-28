import Piece
import Board
import numpy as np

def oppositeCol(col):
    if col == "W":
        return "B"
    else:
        return "W"

def colourToNum(col):
    return 0 if col == " " else (1 if col == "B" else -1)

def sigmoid(z,t): # current activation function
    return 1.0/(1+np.exp(-(z-t)))

class Transpose:

    def __init__(self,score,depth):
        self.score = score
        self.depth = depth

    def getScore(self):
        return self.score
    def getDepth(self):
        return self.depth

MIN_VALUE = -10000000000000000
MAX_VALUE = 10000000000000000

class AI:
    
    def __init__(self,weights1,threshold,weights2):
        
        self.maxDepth = 4
        self.posTranspose = {}
        # weights and threshold used in Neural Network
        self.inputWeights = weights1
        self.hiddenWeights = weights2
        self.threshold = threshold
        # Neural Network has input layer and hidden layer
        self.layer1 = np.zeros((64,1)) # 64 by 1 array of 0s
        self.layer2 = np.zeros((42,1)) # 42 by 1 array of 0s
        

    def makeMove(self,board,col):
        
        moves = board.getAllValidMoves(col)
        bestScore = -1000 # minimum possible
        bestMove = []

        self.posTranspose = {}
        for i in range(len(moves)):
            tempBoard = Board.Board(board)
            tempBoard.move(col,moves[i][0],moves[i][1])
            score = self.alphabeta(tempBoard,col,0,MIN_VALUE,MAX_VALUE,False)
            if score > bestScore:
                bestScore = score
                bestMove = moves[i]

        return bestMove
    
    def posEvaluate(self,board):
        
        for i in range(8):
            for j in range(8):
                colNum = colourToNum(board.getPiece(i,j).getColour())
                self.layer1[8*i+j] = colNum

        self.layer2 = np.dot(self.inputWeights,self.layer1)
        for i in range(42):
            self.layer2[i][0] = sigmoid(self.layer2[i][0],self.threshold[i])

        output = np.dot(self.hiddenWeights,self.layer2)

        return output[0][0]
        

    def alphabeta(self,board,col,depth,alpha,beta,maximizingPlayer):
        
        if depth is None:
            return self.posEvaluate(board) 

        OptimalMove = []

        if maximizingPlayer:
            colour = col
        else:
            colour = oppositeCol(col)
        nextCol = oppositeCol(colour)

        moves = board.getAllValidMoves(colour)
        if len(moves) == 0 or depth == self.maxDepth:
            return self.posEvaluate(board)

        if maximizingPlayer:
            v = MIN_VALUE
            for i in range(len(moves)):
                tempBoard = Board.Board(board)
                tempBoard.move(colour,moves[i][0],moves[i][1])

                trans = self.posTranspose.get(tempBoard)

                if trans is None or depth <= trans.getDepth():                
                    v = max(v,self.alphabeta(tempBoard,nextCol,depth+1,alpha,beta,False))
                    self.posTranspose[tempBoard] = Transpose(v,depth)
                else:
                    v = trans.getScore()
                    
                alpha = max(alpha,v)
                if beta <= alpha:
                    break
            return v

        else:
            v = MAX_VALUE
            for i in range(len(moves)):
                tempBoard = Board.Board(board)
                tempBoard.move(colour,moves[i][0],moves[i][1])
                
                trans = self.posTranspose.get(tempBoard)

                if trans is None or depth <= trans.getDepth():                
                    v = min(v,self.alphabeta(tempBoard,nextCol,depth+1,alpha,beta,True))
                    self.posTranspose[tempBoard] = Transpose(v,depth)
                else:
                    v = trans.getScore()
                    
                beta = min(beta,v)
                if beta <= alpha:
                    break
            return v
