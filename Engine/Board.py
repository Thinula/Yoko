import Piece

def inBounds(num):
    return 0 <= num and num < 8

def oppositeCol(col):
    if col == "W":
        return "B"
    else:
        return "W"

class Board:

    def __init__(self,board = None):
        self.board = [] # 2-D array to hold the 8 by 8 squares of pieces
        if board is not None:
            for i in range(8):
                row = []
                for j in range(8):
                    row.append(board.getPiece(i,j))
                self.board.append(row)
        else:
            for i in range(8):
                row = []
                for j in range(8):
                    row.append(Piece.Piece(" ")) # blank denotes empty piece
                self.board.append(row)

            # place the fixed pieces on the board
            self.board[3][3] = Piece.Piece("W")
            self.board[3][4] = Piece.Piece("B")
            self.board[4][3] = Piece.Piece("B")
            self.board[4][4] = Piece.Piece("W")

    def getPiece(self,rowNum,colNum):
        if inBounds(rowNum) and inBounds(colNum):
            return self.board[rowNum][colNum]
        else:
            return None

    def getPosition(self):
        return Position.Position(self)
        
    # returns if the given square is empty
    def emptySquare(self,rowNum,colNum):
        if inBounds(rowNum) and inBounds(colNum):
            return self.board[rowNum][colNum].getColour() == " "
        else:
            return False
    
    def legalMove(self,playerCol,rowNum,colNum):
        
        if not self.emptySquare(rowNum,colNum):
            return False # can't play on a square with a piece

        for i in range(-1,2):
            for j in range(-1,2):
                if not (i == 0 and j == 0):
                    if self.checkDir(playerCol,rowNum,colNum,i,j):
                        return True
        return False           
        
    def move(self,playerCol,rowNum,colNum):
        
        if self.legalMove(playerCol,rowNum,colNum):
            self.board[rowNum][colNum] = Piece.Piece(playerCol)
            for i in range(-1,2):
                for j in range(-1,2):
                    if not (i == 0 and j == 0):
                        self.captureEnemyPiece(playerCol,rowNum,colNum,i,j)
    
    def captureEnemyPiece(self,playerCol,rowNum,colNum,deltaRow,deltaCol):

        checkRow = rowNum+deltaRow
        checkCol = colNum+deltaCol
        
        emptySquareFound = False
        oppColSquareFound = False

        while inBounds(checkRow) and inBounds(checkCol) and not emptySquareFound:

            currentSquareCol = self.board[checkRow][checkCol].getColour()
            if currentSquareCol == playerCol and oppColSquareFound and not emptySquareFound:
                
                minRow = min(rowNum,checkRow)
                maxRow = max(rowNum,checkRow)
                minCol = min(colNum,checkCol)
                maxCol = max(colNum,checkCol)


                if deltaRow == 0:
                    for j in range(minCol+abs(deltaCol),maxCol,abs(deltaCol)):
                        self.board[rowNum][j] = Piece.Piece(playerCol)
                elif deltaCol == 0:
                    for i in range(minRow+abs(deltaRow),maxRow,abs(deltaRow)):
                        self.board[i][colNum] = Piece.Piece(playerCol)
                else: 
                    for i in range(minRow+abs(deltaRow),maxRow,abs(deltaRow)):
                        for j in range(minCol+abs(deltaCol),maxCol,abs(deltaCol)):
                            if abs(i-rowNum) == abs(j-colNum):
                                self.board[i][j] = Piece.Piece(playerCol)
                break
            
            elif currentSquareCol == oppositeCol(playerCol):
                oppColSquareFound = True
            else:
                emptySquareFound = True

            checkRow += deltaRow
            checkCol += deltaCol

    def getAllValidMoves(self,playerCol):

        moves = [] # array of pairs to hold which coordinates have a valid move
        for i in range(8):
            for j in range(8):
                if self.legalMove(playerCol,i,j):
                    moves.append((i,j))
        return moves

    def gameOver(self):
        # game ends when both players cannot make a move
        blackMoves = self.getAllValidMoves("B")
        whiteMoves = self.getAllValidMoves("W")
        
        return len(blackMoves) == 0 and len(whiteMoves) == 0

    def winner(self):
        if not self.gameOver():
            return None
        else:
            blackPoints = 0
            whitePoints = 0
            
            for i in range(8):
                for j in range(8):
                    piece = self.getPiece(i,j)
                    if piece.getColour() == "B":
                        blackPoints += 1
                    elif piece.getColour() == "W":
                        whitePoints += 1

            return [blackPoints,whitePoints]
    
    def checkDir(self,playerCol,rowNum,colNum,deltaRow,deltaCol):
        
        checkRow = rowNum+deltaRow
        checkCol = colNum+deltaCol
        
        emptySquareFound = False
        oppColSquareFound = False
        sameColSquareFound = False

        while inBounds(checkRow) and inBounds(checkCol) and not sameColSquareFound and not emptySquareFound:

            currentSquareCol = self.board[checkRow][checkCol].getColour()
            if currentSquareCol == playerCol and oppColSquareFound:
                sameColSquareFound = True
            elif currentSquareCol == oppositeCol(playerCol):
                oppColSquareFound = True
            else:
                emptySquareFound = True
 
            checkRow += deltaRow
            checkCol += deltaCol

        return not emptySquareFound and oppColSquareFound and sameColSquareFound

    def __str__(self):
        outStr = "\n\n  "
        for i in range(8):
            if i == 0:
                for j in range(8):
                    outStr += str(j+1) + " "
                outStr += "\n"
            outStr += str(i+1) + " "
            for j in range(8):
                outStr += self.board[i][j].getColour() + " "
            outStr += "\n"
        return outStr








    
