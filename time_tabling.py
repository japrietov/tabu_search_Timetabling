import numpy as np
import random
import itertools

days = {0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday'}
time_slots = {0:'7_9', 1:'9_11', 2:'11_13', 3:'14_16', 4:'16_18', 5:'18_20'}
type_classrooms = {'C':[0,1,2,3], 'N':[4,5,6,7,8,9]}
dict_of_classrooms = {0:('103',60), 1:('203',60), 2:('303',60), 3:('101',45), 4:('102',45), 5:('104',60), 6:('105',45), 7:('106',45), 8:('107',60), 9:('108',45)}

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
    # print dict_possible_combinations_copy
    #indexC = 0
    #indexN = 0
    for dat in data_complete:
        data_split = dat.split(",")
        if data_split[3] == 'C':
            # Choose only the classroom that have more seats that the capability of the course
            configC = []

            copy_copy_copy = dict_possible_combinations_copy['C'][:]
            for comb in dict_possible_combinations_copy['C']:
                if int(data_split[4]) < dict_of_classrooms[comb[2]][1]:

                    # Make the block (Mo - We, Th - Th, We - Fr)
                    tmp__ = None
                    if comb[0] == 0:
                        if (2, comb[1], comb[2]) in copy_copy_copy:
                            tmp__ = (2, comb[1], comb[2])
                        else:
                            for cl in type_classrooms['C']:
                                if (2, comb[1], cl) in copy_copy_copy:
                                    tmp__ = (2, comb[1], cl)
                                    break
                    elif comb[0] == 2:
                        if (0, comb[1], comb[2]) in copy_copy_copy:
                            tmp__ = (0, comb[1], comb[2])
                        else:
                            for cl in type_classrooms['C']:
                                if (0, comb[1], cl) in copy_copy_copy:
                                    tmp__ = (0, comb[1], cl)
                                    break
                    elif comb[0] == 1:
                        tmp__ = (3, comb[1], comb[2])
                    elif comb[0] == 3:
                        tmp__ = (1, comb[1], comb[2])
                    else:
                        if (2, comb[1], comb[2]) in copy_copy_copy:
                            tmp__ = (2, comb[1], comb[2])
                        else:
                            for cl in type_classrooms['C']:
                                if (2, comb[1], cl) in copy_copy_copy:
                                    tmp__ = (2, comb[1], cl)
                                    break

                    copy_copy_copy.pop(copy_copy_copy.index(tmp__))
                    copy_copy_copy.pop(copy_copy_copy.index(comb))

                    configC.append(comb)
                    configC.append(tmp__)

                    # print "C", configC
                    break
            dict_possible_combinations_copy['C'] = copy_copy_copy[:]
            dict_current_configuration[dat] = configC
        else:
            #indexN += 1
            configN = []

            copy_copy = dict_possible_combinations_copy['N'][:]
            for combN in dict_possible_combinations_copy['N']:
                if int(data_split[4]) < dict_of_classrooms[combN[2]][1]:

                    # Make the block (Mo - We, Th - Th, We - Fr)
                    tmp_ = None
                    if combN[0] == 0:
                        if (2, combN[1], combN[2]) in copy_copy:
                            tmp_ = (2, combN[1], combN[2])
                        else:
                            for cl in type_classrooms['N']:
                                if (2, combN[1], cl) in copy_copy:
                                    tmp_ = (2, combN[1], cl)
                                    break
                    elif combN[0] == 2:
                        if (0, combN[1], combN[2]) in copy_copy:
                            tmp_ = (0, combN[1], combN[2])
                        else:
                            for cl in type_classrooms['N']:
                                if (0, combN[1], cl) in copy_copy:
                                    tmp_ = (0, combN[1], cl)
                                    break
                    elif combN[0] == 1:
                        tmp_ = (3, combN[1], combN[2])
                    elif combN[0] == 3:
                        tmp_ = (1, combN[1], combN[2])
                    else:
                        if (2, combN[1], combN[2]) in copy_copy:
                            tmp_ = (2, combN[1], combN[2])
                        else:
                            for cl in type_classrooms['N']:
                                if (2, combN[1], cl) in copy_copy:
                                    tmp_ = (2, combN[1], cl)
                                    break

                    copy_copy.pop(copy_copy.index(tmp_))
                    copy_copy.pop(copy_copy.index(combN))

                    configN.append(combN)
                    configN.append(tmp_)


                    # print "N", configN
                    break
            dict_possible_combinations_copy['N'] = copy_copy[:]
            dict_current_configuration[dat] = configN

    # print indexC, len(dict_possible_combinations_copy['C'])
    # print indexN, len(dict_possible_combinations_copy['N'])

    return dict_current_configuration, dict_possible_combinations_copy


def check_neighborhood(dat):
    if dat[3] == 'C':
        print random.choice(type_classrooms['C'])




############################
# Initialize the program
############################

# Initialize all possibilities we have
possible_combinations()

# 3D matrix (x=weekdays, y=slots, z=classrooms)
matrix_complete = np.chararray((5, len(time_slots.keys()), 10), itemsize=50)
matrix_complete[:] = '------------'

# A tuple in each position of the matrix (name_professor, semester, course, type_of_classroom, capability)
data = open("data.txt").readlines()
data_with_capability = []
for dat in data:
    data_with_capability.append(dat.strip() + "," + str(make_random_capability()))


################################################
# Test the first configuration
################################################

# print dict_possible_combinations

tmp, copy = first_configuration(data_with_capability)

# Assign the values of the first configuration to the matrix.


for j in tmp:
    day1 = tmp[j][0][0]
    slot1 = tmp[j][0][1]
    classroom1 = tmp[j][0][2]
    day2 = tmp[j][1][0]
    slot2 = tmp[j][1][1]
    classroom2 = tmp[j][1][2]

    matrix_complete[day1][slot1][classroom1] = j.split(',')[2]
    matrix_complete[day2][slot2][classroom2] = j.split(',')[2]


    # print j, "|", days[tmp[j][0]], time_slots[tmp[j][1]], dict_of_classrooms[tmp[j][2]], "|", tmp[j]


# Print the matrix complete using only The day "MONDAY"
import pandas as pd


for i in range(len(matrix_complete)):
    print days[i].upper()
    df = pd.DataFrame(matrix_complete[i], index=time_slots.values(), columns=[i[0] for i in dict_of_classrooms.values()])
    print df.to_string()
    print



"""
for weekday in matrix_complete:
    for slot in weekday:
        for classroom in slot:
            dat = 'Aztaiza,4,optimizacion,C,'
            list_atributes = dat.split(',')
            if list_atributes[3] == 'C':
                print random.choice(type_classrooms['C'])
"""

#som = type_classrooms.copy()
#som.pop('C')

#print som
#print type_classrooms
# print matrix_complete



