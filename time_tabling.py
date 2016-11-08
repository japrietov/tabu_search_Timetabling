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
        dict_possible_combinations[key] = list(itertools.product(days, time_slots_list, type_classrooms[key]))
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
            configC = None
            for comb in dict_possible_combinations_copy['C']:
                if int(data_split[4]) < dict_of_classrooms[comb[2]][1]:
                    #configC = random.randint(0,len(dict_possible_combinations_copy['C'])-1))
                    dict_possible_combinations_copy['C'].pop(dict_possible_combinations_copy['C'].index(comb))
                    configC = comb
                    break
            #indexC +=1
            dict_current_configuration[dat] = configC
        if data_split[3] == 'N':
            #indexN += 1
            configN = None
            for comb in dict_possible_combinations_copy['N']:
                if int(data_split[4]) < dict_of_classrooms[comb[2]][1]:
                    #configC = dict_possible_combinations_copy['C'].pop(random.randint(0,len(dict_possible_combinations_copy['C'])-1))
                    dict_possible_combinations_copy['N'].pop(dict_possible_combinations_copy['N'].index(comb))
                    configN = comb
                    break
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
matrix_complete[:] = '-----'

# A tuple in each position of the matrix (name_professor, semester, course, type_of_classroom, capability)
data = open("data.txt").readlines()
data_with_capability = []
for dat in data:
    data_with_capability.append(dat.strip() + "," + str(make_random_capability()))


################################################
# Test the first configuration
################################################

print dict_possible_combinations

tmp, copy = first_configuration(data_with_capability)

# Assign the values of the first configuration to the matrix.
for j in tmp:
    day = tmp[j][0]
    slot = tmp[j][1]
    classroom = tmp[j][2]
    matrix_complete[day][slot][classroom] = j.split(',')[2]
    # print j, "|", days[tmp[j][0]], time_slots[tmp[j][1]], dict_of_classrooms[tmp[j][2]], "|", tmp[j]


# Print the matrix complete using only The day "MONDAY"
import pandas as pd
df = pd.DataFrame(matrix_complete[0], index=time_slots.values(), columns=[i[0] for i in dict_of_classrooms.values()])
print df



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



