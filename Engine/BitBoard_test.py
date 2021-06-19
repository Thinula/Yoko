import BitBoard
import AI
import time
start_time = time.time()


AIWhite = AI.AI()
AIBlack = AI.AI()
board = BitBoard.BitBoard()

gameRecord = open("Test.txt","w")
turn = 0
while not board.gameOver():
    gameRecord.write(str(board))
    print(board)
    playerCol = "B" if turn%2 == 0 else "W"

    if turn % 2 == 0:
        nextMove = AIBlack.makeMove(board,playerCol)
    else:
        nextMove = AIWhite.makeMove(board,playerCol)

    if 0 <= nextMove and nextMove < 64:
        board.makeMove(playerCol,nextMove)

    turn += 1
print("--- %s seconds ---" % (time.time() - start_time))   
