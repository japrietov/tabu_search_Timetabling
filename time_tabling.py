import numpy as np
import random
import itertools

days = {0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday'}
time_slots = {0:'7_9', 1:'9_11', 2:'11_13', 3:'14_16', 4:'16_18', 5:'18_20'}
type_classrooms = {'C':[0,1,2,3,4], 'N':[5,6,7,8,9]}
dict_of_classrooms = {0:('103',60), 1:('203',60), 2:('303',60), 3:('101',45), 4:('102',45), 5:('104',60), 6:('105',45), 7:('106',45), 8:('107',60), 9:('108',45)}


dict_of_data = {}


# key=Type of classroom(C,N), values=possible combinations of slots and classrooms((day0, slot0,classroom0), (day0, slot1,classroom1))
dict_possible_combinations = {}

# key=dat(Aztaiza,6,optimizacion,C), values=possible combination
dict_current_configuration = {}

# Create a random capability of each class from a random distribution
def make_random_capability():
    return random.randint(30,50)

# Make all possible combinations of a time_slot and the dictionary of classrooms
def possible_combinations():
    time_slots_list = time_slots.keys()
    for key in type_classrooms:
        tmp_product = list(itertools.product(days, time_slots_list, type_classrooms[key]))
        random.shuffle(tmp_product)
        dict_possible_combinations[key] = tmp_product
    return dict_possible_combinations

# Choose a random configuration for each course. This random configuration will be the first configuration
def first_configuration(data_complete):
    dict_possible_combinations_copy = dict_possible_combinations.copy()

    for dat in data_complete:
        data_split = data_complete[dat][0].split(",")
        if data_split[3] == 'C':
            # Choose only the classroom that have more seats that the capability of the course
            configC = []

            copy_copy_copy = dict_possible_combinations_copy['C'][:]
            for comb in dict_possible_combinations_copy['C']:
                if int(data_split[4]) < dict_of_classrooms[comb[2]][1]:

                    pass_var_C = True

                    # Make the block (Mo - We, Th - Th, We - Fr)
                    tmp__ = None
                    if comb[0] == 0:
                        tmp__ = (2, comb[1], comb[2])
                    elif comb[0] == 2:
                        tmp__ = (0, comb[1], comb[2])
                    elif comb[0] == 1:
                        tmp__ = (3, comb[1], comb[2])
                    elif comb[0] == 3:
                        tmp__ = (1, comb[1], comb[2])
                    else:
                        if (2, comb[1], comb[2]) in copy_copy_copy:
                            tmp__ = (2, comb[1], comb[2])
                            copy_copy_copy.pop(copy_copy_copy.index((0, comb[1], comb[2])))
                        else:
                            pass_var_C = False

                    if pass_var_C:
                        copy_copy_copy.pop(copy_copy_copy.index(tmp__))
                        copy_copy_copy.pop(copy_copy_copy.index(comb))

                        configC.append(comb)
                        configC.append(tmp__)

                        break

            dict_possible_combinations_copy['C'] = copy_copy_copy[:]
            dict_current_configuration[dat] = [data_complete[dat][0]] + configC
        else:
            configN = []

            copy_copy = dict_possible_combinations_copy['N'][:]
            for combN in dict_possible_combinations_copy['N']:
                if int(data_split[4]) < dict_of_classrooms[combN[2]][1]:

                    pass_var_N = True

                    # Make the block (Mo - We, Th - Th, We - Fr)
                    tmp_ = None
                    if combN[0] == 0:
                        tmp_ = (2, combN[1], combN[2])
                    elif combN[0] == 2:
                        tmp_ = (0, combN[1], combN[2])
                    elif combN[0] == 1:
                        tmp_ = (3, combN[1], combN[2])
                    elif combN[0] == 3:
                        tmp_ = (1, combN[1], combN[2])
                    else:
                        if (2, combN[1], combN[2]) in copy_copy:
                            tmp_ = (2, combN[1], combN[2])
                            copy_copy.pop(copy_copy.index((0, combN[1], combN[2])))
                        else:
                            pass_var_N = False

                    if pass_var_N:
                        copy_copy.pop(copy_copy.index(tmp_))
                        copy_copy.pop(copy_copy.index(combN))

                        configN.append(combN)
                        configN.append(tmp_)

                        break

            dict_possible_combinations_copy['N'] = copy_copy[:]
            dict_current_configuration[dat] = [data_complete[dat][0]] + configN

    return dict_current_configuration, dict_possible_combinations_copy

# All possible neighbors
dict_possible_neighbors = {'C':[], 'N':[]}
def possible_neighbors(possible_combinations):

    # Possible combinations of C classroom
    c_possible_combinations = possible_combinations['C']
    copy_c_possible_MJ = c_possible_combinations[:]
    copy_c_possible_LM = c_possible_combinations[:]
    copy_c_possible_MV = c_possible_combinations[:]
    for possible in c_possible_combinations:
        if possible[0] == 1:
            day1 = copy_c_possible_MJ.pop(copy_c_possible_MJ.index(possible))
            day2 = copy_c_possible_MJ.pop(copy_c_possible_MJ.index((3,possible[1], possible[2])))
            dict_possible_neighbors['C'].append([day1,day2])
        if possible[0] == 2:
            day1_LM = copy_c_possible_LM.pop(copy_c_possible_LM.index(possible))
            day2_LM = copy_c_possible_LM.pop(copy_c_possible_LM.index((0, possible[1], possible[2])))
            dict_possible_neighbors['C'].append([day1_LM, day2_LM])
            day1_MV = copy_c_possible_MV.pop(copy_c_possible_MV.index(possible))
            day2_MV = copy_c_possible_MV.pop(copy_c_possible_MV.index((4, possible[1], possible[2])))
            dict_possible_neighbors['C'].append([day1_MV, day2_MV])

    # Possible combinations of N classroom
    n_possible_combinations = possible_combinations['N']
    copy_n_possible_MJ = n_possible_combinations[:]
    copy_n_possible_LM = n_possible_combinations[:]
    copy_n_possible_MV = n_possible_combinations[:]
    for possible_n in n_possible_combinations:
        if possible_n[0] == 1:
            day1_n = copy_n_possible_MJ.pop(copy_n_possible_MJ.index(possible_n))
            day2_n = copy_n_possible_MJ.pop(copy_n_possible_MJ.index((3,possible_n[1], possible_n[2])))
            dict_possible_neighbors['N'].append([day1_n,day2_n])
        if possible_n[0] == 2:
            day1_LM_n = copy_n_possible_LM.pop(copy_n_possible_LM.index(possible_n))
            day2_LM_n = copy_n_possible_LM.pop(copy_n_possible_LM.index((0, possible_n[1], possible_n[2])))
            dict_possible_neighbors['N'].append([day1_LM_n, day2_LM_n])
            day1_MV_n = copy_n_possible_MV.pop(copy_n_possible_MV.index(possible_n))
            day2_MV_n = copy_n_possible_MV.pop(copy_n_possible_MV.index((4, possible_n[1], possible_n[2])))
            dict_possible_neighbors['N'].append([day1_MV_n, day2_MV_n])


############################
# Initialize the program
############################

# A tuple in each position of the matrix (name_professor, semester, course, type_of_classroom, capability)
data = open("data.txt").readlines()
data_with_capability = []
for dat in data:
    data_with_capability.append(dat.strip() + "," + str(make_random_capability()))


for index in range(len(data_with_capability)):
    dict_of_data[index] = [data_with_capability[index]]

# Initialize all possibilities we have
possible_combinations()
possible_neighbors(dict_possible_combinations)

# 3D matrix (x=weekdays, y=slots, z=classrooms)
matrix_complete = np.zeros((len(days.keys()), len(time_slots.keys()), len(dict_of_classrooms.keys())), dtype='Int32')

################################################
# Test the first configuration
################################################

tmp, copy = first_configuration(dict_of_data)

# Assign the values of the first configuration to the matrix.
for j in tmp:
    day1 = tmp[j][1][0]
    slot1 = tmp[j][1][1]
    classroom1 = tmp[j][1][2]
    day2 = tmp[j][2][0]
    slot2 = tmp[j][2][1]
    classroom2 = tmp[j][2][2]

    matrix_complete[day1][slot1][classroom1] = j
    matrix_complete[day2][slot2][classroom2] = j


# Save the dictionary of first configuration
np.save('first_conf_dict.npy', dict_current_configuration)
np.save('first_conf_matrix.npy', matrix_complete)
np.save('possible_combinations_dict.npy', dict_possible_combinations)
np.save('possible_neighbors_dict.npy', dict_possible_neighbors)

# TO PRINT A MATRIX
"""
# Print the matrix complete using only The day "MONDAY"
import pandas as pd


for i in range(len(matrix_complete)):
    print days[i].upper()
    df = pd.DataFrame(matrix_complete[i], index=time_slots.values(), columns=[i[0] for i in dict_of_classrooms.values()])
    print df.to_string()
    print
"""

