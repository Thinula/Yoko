import Piece
import Board
import AI
import numpy as np
import random

def Game(player1, player2):
    
    gameRecord = open("Test.txt","w")
    board = Board.Board()
    moves = [(1,2)] # initialized with a pair to get through first while loop
    turn = 0

    while len(moves) != 0:
        gameRecord.write(str(board))
        
        if turn % 2 == 0:
            playerCol = "B"
            nextMove = player1.makeMove(board,playerCol)
        else:
            playerCol = "W"
            nextMove = player2.makeMove(board,playerCol)

        moves = board.getAllValidMoves(playerCol)
        print(playerCol)
        if len(nextMove) == 2: # if a move has been made
            board.move(playerCol,nextMove[0],nextMove[1])
            turn += 1
            
        print(board)
        print(nextMove)
        
        if len(nextMove) != 2:
            print(board.gameOver())
        if len(nextMove) != 2 and not board.gameOver():
            moves = [1] # so the loop doesn't end
            turn += 1

        if board.gameOver():
            arr = board.winner()
            if arr[0] == arr[1]:
                return 0
            elif arr[0] > arr[1]:
                return 1
            else:
                return -1

def Tournament(arrayOfPlayers):

    scores = []
    for i in range(len(arrayOfPlayers)):
        nums = [0,i]
        scores.append(nums)

    for i in range(len(arrayOfPlayers)):
        for j in range(i):
            game = Game(arrayOfPlayers[i],arrayOfPlayers[j])
            scores[i][0] += game #random.randint(0,1)
            scores[j][0] -= game #random.randint(0,1)

            game = Game(arrayOfPlayers[j],arrayOfPlayers[i])
            scores[i][0] -= game
            scores[j][0] += game

    scores.sort()
    N = int(len(arrayOfPlayers)/2)
    for i in range(N):
        scores[i+N] = scores[i]

    return scores

players = []
for i in range(24):
    temp1 = np.array([np.random.normal(0,1,64)]) # 1 by 64 array
    temp2 = np.array([np.random.normal(0,1,42)]) # 1 by 42 array
    temp2 = np.transpose(temp2)

    weights1 = np.dot(temp2,temp1) # 42 by 64 array
    weights2 = np.array([np.random.normal(0,1,42)]) # 1 by 42 array
    thresh   = np.array([np.random.normal(0,1,42)]) # 1 by 42 array
    thresh = np.transpose(thresh)
    players.append(AI.AI(weights1,thresh,weights2))
    
print(Tournament(players))



