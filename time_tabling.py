import numpy as np
import random
import itertools


time_slots = {0:'7_9', 1:'9_11', 2:'11_13', 4:'14_16', 5:'16_18', 6:'18_20'}
type_classrooms = {'C':[0,1,2,3,4], 'N':[5,6,7,8,9]}
dict_of_classrooms = {0:('103',60), 1:('203',60), 2:('303',60), 3:('101',30), 4:('102',30), 5:('104',60), 6:('105',30), 7:('106',30), 8:('107',60), 9:('108',30)}

# key=Type of classroom(C,N), values=possible combinations of slots and classrooms((slot0,classroom0), (slot1,classroom1))
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
        dict_possible_combinations[key] = list(itertools.product(time_slots_list, type_classrooms[key]))
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
            configC = dict_possible_combinations_copy['C'].pop(random.randint(0,len(dict_possible_combinations_copy['C'])-1))
            #indexC +=1
            dict_current_configuration[dat] = configC
        if data_split[3] == 'N':
            #indexN += 1
            configN = dict_possible_combinations_copy['N'].pop(random.randint(0, len(dict_possible_combinations_copy['N'])-1))
            dict_current_configuration[dat] = configN

    # print indexC, len(dict_possible_combinations_copy['C'])
    # print indexN, len(dict_possible_combinations_copy['N'])

    return dict_current_configuration


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
matrix_complete[:] = 'a'

# A tuple in each position of the matrix (name_professor, semester, course, type_of_classroom, capability)
data = open("data.txt").readlines()
data_with_capability = []
for dat in data:
    data_with_capability.append(dat.strip() + "," + str(make_random_capability()))


print first_configuration(data_with_capability)


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



