import os
import BitBoard

def create_files(year, output_folder):
    file_name = "../GameRecords/WTH_" + str(year) + ".txt"
    file = open(file_name, mode="r")

    folder = "../GameRecords/" + output_folder
    if os.path.exists(folder):
        count = len(os.listdir(folder)) + 1
    else:
        count = 1
        print("Folder did not exist!")
    print(count)
    #return

    lines = file.read().splitlines()
    for line in lines:
        file_name = "../GameRecords/" + output_folder + "/Game " + str(count) + ".txt"
        try:
            game_file = open(file_name, mode="w")
        except:
            os.mkdir("../GameRecords/" + output_folder)
            game_file = open(file_name, mode="w")

        #print(line)
        assert(len(line) <= 120)

        board = BitBoard.BitBoard()
        moves = [line[i:i+2] for i in range(0, len(line), 2)]
        colour = "B"
        for move in moves:
            col = ord(move[0]) - ord("A")
            row = int(move[1]) - 1
            index = 8 * row + col
            board.makeMove(colour, index)
        
            game_file.write(move + "\n")
            game_file.write(board.to_string(verbose=False) + "\n")
            colour = "W" if colour == "B" else "B"
        
        count += 1
        result = board.winner()
        if result is not None:
            game_file.write(result)
        
        game_file.close()



year = int(input("Enter the year: "))
file_name = "../GameRecords/WTH_" + str(year) + ".txt"
output_folder = "Games" # str(year)
create_files(year, output_folder)
