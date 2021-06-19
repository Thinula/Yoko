import os
import BitBoard

def equivalent_board_strings(string_one, string_two):
    
    pass

def update_hash(move_dict, posn, result, line_max):
    if result == "B":
        result_tuple = (1, 0)
    elif result == "W":
        result_tuple = (0, 1)
    elif result == "Tie":
        result_tuple = (0.5, 0.5)
    else:
        return move_dict

    if move_dict.get(posn) is None:
        move_dict[posn] = (result_tuple[0], result_tuple[1], line_max)
    else:
        old_tuple = move_dict[posn]
        move_dict[posn] = (old_tuple[0] + result_tuple[0],
                           old_tuple[1] + result_tuple[1],
                           old_tuple[2])
    return move_dict

# generate the dicitionary to hold the moves in the dataset
arr_dicts = []
line_nums = [0 for i in range(64)]
for move in range(60):
    move_dict = {}
    file_name = "Dataset/Move " + str(move+1) + ".txt"

    # makes the file if not created
    try:
        move_file = open(file_name)
    except IOError as e:
        print("Hello! Move " + str(move))
        move_file = open(file_name, mode="w+")

    lines = move_file.read().splitlines()
    line_nums[move] = len(lines) # number of lines in the file
    line_count = 0 # keeps track of line number to edit later
    for line in lines:
        state, black_win, white_win = line.split()
        move_dict[state] = (float(black_win), float(white_win), line_count)
        line_count += 1
        
    arr_dicts.append(move_dict)
    
print(arr_dicts[2])
#pass
# go through all the games
year = int(input("Print year number: "))
folder_name = "../GameRecords/" + str(year)
files = sorted(os.listdir(path=folder_name))

print("Updating Dictionaries now..")
for file_name in files:
    file = open(folder_name + "/" + file_name, mode="r")
    lines = file.read().splitlines()
    result = lines[len(lines)-1]
    move_num = 0
    for line in lines:
        if len(line) == 64:
            arr_dicts[move_num] = update_hash(move_dict=arr_dicts[move_num],
                                              posn=line,
                                              result=result,
                                              line_max=line_nums[move_num])
            # if this position is new, update the line count in the file
            if arr_dicts[move_num].get(line) is not None:
                if arr_dicts[move_num][line][2] == line_nums[move_num]:
                    line_nums[move_num] += 1
            move_num += 1
            
    for move_dict in arr_dicts:
        #print(move_dict)
        pass
    file.close()

print("Finished updating the Dictionaries.")
print("Writing to Files now...")
for move in range(len(arr_dicts)):
    move_dict = dict(sorted(arr_dicts[move].items(), key=lambda item: item[1][2]))
    dict_list = move_dict.items()
    write_list = []
    for elem in dict_list:
        new_elem = elem[0] + " " + str(elem[1][0]) + " " + str(elem[1][1])
        write_list.append(new_elem + "\n")
        #print(elem)

    file = open("Dataset/Move " + str(move+1) + ".txt", mode="w+")
    file.writelines(write_list)
    file.close()

print("Finished writing to Files.")
