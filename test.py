import numpy as np

days = {0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday'}
time_slots = {0:'7_9', 1:'9_11', 2:'11_13', 3:'14_16', 4:'16_18', 5:'18_20'}
type_classrooms = {'C':[0,1,2,3,4], 'N':[5,6,7,8,9]}
dict_of_classrooms = {0:('103',60), 1:('203',60), 2:('303',60), 3:('101',45), 4:('102',45), 5:('104',60), 6:('105',45), 7:('106',45), 8:('107',60), 9:('108',45)}

# Load the first configuration
dict_first_conf = np.load('first_conf_dict.npy').item()
matrix_first_conf = np.load('first_conf_matrix.npy')
possible_combinations = np.load('possible_combinations_dict.npy').item()
dict_possible_neighbors = np.load('possible_neighbors_dict.npy').item()

# Find the possible neighbors in the iteration
def find_neighbors(current_matrix):
    c_possible_neighbors = dict_possible_neighbors['C']
    n_possible_neighbors = dict_possible_neighbors['N']


    dat_neighbors_N = [possible_n for possible_n in n_possible_neighbors if current_matrix.item(possible_n[0]) == current_matrix.item(possible_n[1])]
    dat_neighbors_C = [possible_c for possible_c in c_possible_neighbors if current_matrix.item(possible_c[0]) == current_matrix.item(possible_c[1])]

    dict_current_neighbors = {'C':dat_neighbors_C, 'N':dat_neighbors_N}

    return dict_current_neighbors

print find_neighbors(matrix_first_conf)
