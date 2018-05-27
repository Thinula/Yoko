
class BitBoard:

    def __init__(self, board=None):
        self.blackDiscs = 0
        self.whiteDiscs = 0

        if board is None:
            self.setCell(3,4,"B")
            self.setCell(4,3,"B")
            self.setCell(3,3,"W")
            self.setCell(4,4,"W")

        else:
            self.blackDiscs = board.getBlackDiscs()
            self.whiteDiscs = board.getWhiteDiscs()
        
    # sets cell specified by row and col to colour playerCol
    def setCell(self,row,col,playerCol):
        mask = 1 << (row*8+col)
        self.blackDiscs &= ~mask
        self.whiteDiscs &= ~mask

        if playerCol == "B":
            self.blackDiscs |= mask
        else:
            self.whiteDiscs |= mask

    # returns colour of cell specified by row and col
    def getCell(self,row,col):
        mask = 1 << (row*8+col) # shifts the board by row*8+col

        if self.blackDiscs & mask:
            return "B"
        elif self.whiteDiscs & mask:
            return "W"
        else:
            return " "
        
    def getBlackDiscs(self):
        return self.blackDiscs

    def getWhiteDiscs(self):
        return self.whiteDiscs

    def getDiscs(self,playerCol):
        return self.getBlackDiscs() if playerCol == "B" else self.getWhiteDiscs()
    # shifts disks in direction direct (not really sure how this works?)
    def shift(self,discs,direct):
        masks = [
                9187201950435737471, # Right
                35887507618889599, # Down-right. 
                18446744073709551615, # Down. 
                71775015237779198, # Down-left.
                18374403900871474942, # Left. 
                18374403900871474688, # Up-left.
                18446744073709551615, # Up. 
                9187201950435737344  # Up-right. 
                ]
        leftShifts = [
                0, # Right
                0, # Down-right. 
                0, # Down. 
                0, # Down-left.
                1, # Left. 
                9, # Up-left.
                8, # Up. 
                7  # Up-right. 
                ]
        rightShifts = [
                1, # Right
                9, # Down-right. 
                8, # Down. 
                7, # Down-left.
                0, # Left. 
                0, # Up-left.
                0, # Up. 
                0  # Up-right. 
                ]
        if direct < 4:
            return (discs >> rightShifts[direct]) & masks[direct]
        else:
            return (discs << leftShifts[direct]) & masks[direct]
        
    def getAllValidMoves(self,playerCol):
        emptyCells = ~(self.blackDiscs | self.whiteDiscs)

        if playerCol == "B":
            playerDiscs = self.blackDiscs
            oppDiscs = self.whiteDiscs
        else:
            playerDiscs = self.whiteDiscs
            oppDiscs = self.blackDiscs

        legalMoves = 0    
        for direct in range(8):
            # all opponent discs adjacent to player's disc in direction direct
            moves = self.shift(playerDiscs,direct) & oppDiscs

            # add all opponent discs adjacent to player disc (max 7 times)
            moves |= self.shift(moves,direct) & oppDiscs
            moves |= self.shift(moves,direct) & oppDiscs
            moves |= self.shift(moves,direct) & oppDiscs
            moves |= self.shift(moves,direct) & oppDiscs
            moves |= self.shift(moves,direct) & oppDiscs

            # all legal moves will be intersection with empty cells
            legalMoves |= self.shift(moves,direct) & emptyCells

        return legalMoves

    def legalMove(self,playerCol,row,col):
        mask = 1 << (row*8+col)
        return (self.getAllValidMoves(playerCol) & mask) != 0

    def gameOver(self):
        return self.getAllValidMoves("B") == 0 and self.getAllValidMoves("W") == 0

    def makeMove(self,playerCol,index):
        newDisc = 1 << index
        capturedDiscs = 0
        if playerCol == "B":
            playerDiscs = self.blackDiscs
            oppDiscs = self.whiteDiscs
        else:
            playerDiscs = self.whiteDiscs
            oppDiscs = self.blackDiscs

        playerDiscs |= newDisc
        for direct in range(8):
            moves = self.shift(newDisc,direct) & oppDiscs
            
            moves |= self.shift(moves,direct) & oppDiscs
            moves |= self.shift(moves,direct) & oppDiscs
            moves |= self.shift(moves,direct) & oppDiscs
            moves |= self.shift(moves,direct) & oppDiscs
            moves |= self.shift(moves,direct) & oppDiscs

            # now determine if discs were caputred
            boundingDiscs = self.shift(moves,direct) & playerDiscs
            if boundingDiscs == 0:
                capturedDiscs |= 0
            else:
                capturedDiscs |= moves
                
        self.blackDiscs = playerDiscs if playerCol == "B" else oppDiscs
        self.whiteDiscs = playerDiscs if playerCol == "W" else oppDiscs
        self.blackDiscs ^= capturedDiscs
        self.whiteDiscs ^= capturedDiscs
        
    def __str__(self):
        outStr = "\n\n  "
        for i in range(8):
            if i == 0:
                for j in range(8):
                    outStr += str(j+1) + " "
                outStr += "\n"
            outStr += str(i+1) + " "
            for j in range(8):
                outStr += self.getCell(i,j) + " "
            outStr += "\n"
        return outStr












                









    
    
