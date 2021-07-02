import os
import BitBoard
import csv
import numpy as np

def equivalent_board_strings(string_one, string_two):
    
    pass

def convert_move_to_index(move):
    col = ord(move[0]) - ord("A")
    row = int(move[1]) - 1
    return 8 * row + col

def indicator_array(move):
    arr = [0 for i in range(64)]
    arr[move] = 1
    return arr

def convert_state_to_data(curr_posn, move, count, test=False):
    state_data = [count]
    for i in range(len(curr_posn)):
        if curr_posn[i] == "B":
            state_data.append(1)
        elif curr_posn[i] == "W":
            state_data.append(-1)
        elif curr_posn[i] == "X":
            state_data.append(0)
        else:
            print("RIP!")

    if test:
        assert(len(move) == 64)
        for i in range(len(move)):
            state_data.append(move[i])
    else:
        state_data.append(move)
    return state_data


games_count = len(os.listdir("../GameRecords/Games"))
training_size = int(games_count * 0.7)
print(games_count, training_size)


# read game files and translate to a dataset
board = BitBoard.BitBoard()
curr_posn = board.to_string(verbose=False)
field_names = ["Posn #"] + ["Feature " + str(i+1) for i in range(64)]
print(field_names)
training_data = []
testing_data = []
prob_diction = {} # gets the probability distribution of P(A | S) 
count = 1

# extract data from the game files
for game in range(games_count):
    file = open("../GameRecords/Games/Game " + str(game+1) + ".txt", mode="r")
    lines = file.read().splitlines()

    # Handles the first state
    curr_posn = board.to_string(verbose=False)

    for line in lines:
        if len(line) == 2:
            move = convert_move_to_index(line)
            state_data = convert_state_to_data(curr_posn, move, count)
            # update the probability distribution totals
            if prob_diction.get(curr_posn) is None:
                prob_diction[curr_posn] = indicator_array(move)
            else:
                prob_diction[curr_posn] = list(np.add(prob_diction[curr_posn], indicator_array(move)))

            if game < training_size:
                training_data.append(state_data)
            count += 1

        elif len(line) == 64:
            curr_posn = line

count = 1
# extract the testing data from the game files
for game in range(training_size, games_count):
    file = open("../GameRecords/Games/Game " + str(game+1) + ".txt", mode="r")
    lines = file.read().splitlines()

    # Handles the first state
    curr_posn = board.to_string(verbose=False)

    for line in lines:
        if len(line) == 2:
            total = sum(prob_diction[curr_posn])
            prob_diction[curr_posn] = [float(num)/total for num in prob_diction[curr_posn]]

            state_data = convert_state_to_data(curr_posn, list(prob_diction[curr_posn]), count, True)
            testing_data.append(state_data)
            count += 1

        if len(line) == 64:
            curr_posn = line

# write data to the csv file
with open(name="Policy Dataset/training_data.csv", mode="w") as f:
    train_field_names = field_names + ["Label"]
    writer = csv.writer(f)
    writer.writerow(train_field_names)
    writer.writerows(training_data)

# write data to the csv file
with open(name="Policy Dataset/testing_data.csv", mode="w") as f:
    test_field_names = field_names + ["Label " + str(i+1) for i in range(64)]
    writer = csv.writer(f)
    writer.writerow(test_field_names)
    writer.writerows(testing_data)


