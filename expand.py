import numpy as np
import itertools

#this definition finds the number of variables present in the boolean expression and also it gives the list of variables
def list_of_var(fnc):
    var_list = []
    for lit in fnc:
        if lit == '+':
            continue

        #adding only the true form into the var_list if it is not already present
        elif lit.isupper():
            if(lit.lower() not in var_list):
                var_list.append(lit.lower())
            else: 
                continue

        #adding only the true form into the var_list if it is not already present
        elif lit.islower():
            if(lit not in var_list):
                var_list.append(lit)
            else: 
                continue
    return var_list

#This definition converts the given boolean function into Positional cube notation
def fnc_pcn(fnc, var_list):
    fnc_split = fnc.split('+')
    #creates a dictionary with keys as cubes of the function
    pcn_dict = dict.fromkeys(fnc_split, [])
    num_var = len(var_list)
    for cube in fnc_split:
        #intializes pcn of that cube to all 1's
        pcn_dict[cube] = [1] * (2*num_var)
        for lit in cube:
            #if the literal is in complement form, it matches its position in var_list and updates the pcn accordingly with 10
            if lit.isupper():
                index = var_list.index(lit.lower())
                pcn_dict[cube][2*index] = 1
                pcn_dict[cube][2*index + 1] = 0
            #if the literal is in true form, it matches its position in var_list and updates the pcn accordingly with 01
            else:
                index = var_list.index(lit)
                pcn_dict[cube][2*index] = 0
                pcn_dict[cube][2*index + 1] = 1

    return(pcn_dict)

#This definition finds the weight of the cubes and sort the cubes as per the weight
def cubes_sort(fnc, pcn_dict, var_list):
    fnc_split = fnc.split('+')
    num_var = len(var_list)
    sum_cols_temp = []

    for i in range(0, 2*num_var):
        sum_temp = sum(value[i] for value in pcn_dict.values())
        sum_cols_temp.append(sum_temp)
    pcn_matrix_temp = list(pcn_dict.values())
    #Two matrices are created to find the product that finds the weight
    pcn_matrix = np.array(pcn_matrix_temp)
    sum_cols = np.array(sum_cols_temp)
    weights = list(np.dot(pcn_matrix, sum_cols))
    print("Weights of the cubes: ", weights)

    #creating the sorted list of cubes
    weights_sort = sorted(weights)
    cubes_list_sorted = []
    for weight in weights_sort:
        index = weights.index(weight)
        weights.remove(weights[index])  
        cubes_list_sorted.append(fnc_split[index])
        fnc_split.remove(fnc_split[index])

    return cubes_list_sorted

#This definition finds the intersection of two cubes denoted in PCN
def intersection(a_list, b_list):
    c_list = []
    for i in range(len(a_list)):
        c_list.append(a_list[i] & b_list[i])
    
    return c_list

#This definition is to find the complement of each element of PCN notation of a cube
def complement_pcn(a_list):
    b_list = []
    for i in range(0, len(a_list)):
        if a_list[i] == 1:
            b_list.append(0)
        elif a_list[i] == 0:
            b_list.append(1)
    
    return b_list

#This definition is to find the complement of a cube using SHARP operator i.e. 1 # b_list
def comp_by_sharp(b_list):
    num_of_pos = len(b_list)
    a_list = num_of_pos*[1]
    num_of_pos_half = int(num_of_pos/2)
    c_list = [[1 for j in range(num_of_pos)] for i in range(num_of_pos_half)]
    temp = []
    for i in range(0, num_of_pos_half):
        temp.append(intersection([a_list[2*i], a_list[2*i+1]], complement_pcn([b_list[2*i], b_list[2*i+1]])))
        c_list[i][2*i] = temp[i][0]
        c_list[i][2*i+1] = temp[i][1]
    
    return c_list

#This definition is find the intersection of two functions with multiple cubes.
def intersection_mul(a_list, b_list):
    c_list = []
    for i in range(0, len(a_list)):
        for j in range(0, len(b_list)):
            c_list.append(intersection(a_list[i], b_list[j]))

    return c_list

#This definition is find the complement of all the cubes of a function
def complement_cubes(fnc_dict):
    fnc_dict_cube_comp = {}
    for key in fnc_dict:
        fnc_dict_cube_comp[key] = comp_by_sharp(fnc_dict[key])
    
    return fnc_dict_cube_comp

#This definition is to find the complement of the function by intersecting the complements of cubes.
def complement_fnc(fnc_dict_cube_comp, var_list):
    fnc_comp = []
    cubes = list(fnc_dict_cube_comp.keys())
    temp_cube = fnc_dict_cube_comp[cubes[0]]
    for i in range(1, len(cubes)):
        temp_cube = intersection_mul(temp_cube, fnc_dict_cube_comp[cubes[i]]) 
    for i in range(0, len(temp_cube)):
        if temp_cube[i] not in fnc_comp:
            fnc_comp.append(temp_cube[i])
        else:
            continue
    #Void cubes are deleted
    flag = 0
    for i in range(0, len(fnc_comp)):
        for j in range(0, len(var_list)):
            if fnc_comp[i-flag][2*j] == fnc_comp[i-flag][2*j+1] == 0:
                fnc_comp.remove(fnc_comp[i-flag])
                flag = flag+1
                break
    return fnc_comp 

#This definition coverts the PCN notation to strin format for display
def pcn_fnc_comp(fnc_comp, var_list):
    fnc_bar = ""
    for i in range(0, len(fnc_comp)):
        for j in range(0, len(var_list)):
            if fnc_comp[i][2*j] == 1 and fnc_comp[i][2*j+1] == 0:
                fnc_bar = fnc_bar + var_list[j].upper()
            elif fnc_comp[i][2*j] == 0 and fnc_comp[i][2*j+1] == 1:
                fnc_bar = fnc_bar + var_list[j]
            elif fnc_comp[i][2*j] == 1 and fnc_comp[i][2*j+1] == 1:
                continue
        fnc_bar = fnc_bar + "+"
    
    fnc_bar = fnc_bar[:-1]
    return fnc_bar

#This definition finds the blocing matrix of the cubes with respect to fbar
def blocking_matrix(cube, fn_bar):
    fn_bar_split = fn_bar.split('+')
    no_comp_cubes = len(fn_bar_split)
    no_cube_lit = len(cube)
    #A matrix with all entries as 0s is created.
    b_matrix = [[0 for j in range(no_comp_cubes)] for i in range(no_cube_lit)]
    #If lit is present as complemeted form in the cube of fbar, then 1 is added to that respective element
    for lit in range(0, no_cube_lit):
        for comp_cube in range(0, no_comp_cubes):
            if cube[lit].isupper():
                if cube[lit].lower() in fn_bar_split[comp_cube]:
                    b_matrix[lit][comp_cube] = 1
                else:
                    continue
            elif cube[lit].islower():
                if cube[lit].upper() in fn_bar_split[comp_cube]:
                    b_matrix[lit][comp_cube] = 1
                else:
                    continue
    
    return b_matrix

#This definition is to generate all possible combination of rows.
def generate_combs(nums):
    result = []
    n = len(nums)

    for r in range(1, n+1):
        combinations = list(itertools.combinations(nums, r))
        result.extend(combinations)

    return result

#This definition is solve the covering problem of the blocking matrix
def covering(cube, b_matrix):
    rows = len(b_matrix)
    cols = len(b_matrix[0])
    row_list = list(range(0, rows))
    comb_list = generate_combs(row_list)
    #All the rows in a combination are added and then checks if it contains a 0. 
    #If yes, then it is continued else, that combination is returned.
    for comb in comb_list:
        temp = [0]*cols
        for row in comb:
            for i in range(0, cols):
                temp[i] = temp[i] + b_matrix[row][i]
        if 0 not in temp:
            break
    
    expanded_cube = ""
    for i in comb:
        expanded_cube = expanded_cube + cube[i]

    return expanded_cube

fon = input("Enter the ON set: ")
fdc = input("Enter the DC set. If there is no DC set, enter n. ")
#creating a new function with both ON set and DC set to find complement
if fdc.upper() != "N":
    fondc = fon + "+" + fdc
else:
    fondc = fon
fondc_split = fondc.split("+")
print("Cover of the function: " , fondc_split)
#creates a list of variables
var_list = list_of_var(fondc)
#creates positional cube notation for ON set
pcn_on = fnc_pcn(fon, var_list)
print(pcn_on)
#creates positional cube notation for ON set and DC set to find complement
#fnc_bar is the complement of the function
pcn_ondc = fnc_pcn(fondc, var_list)
cubes_comp = complement_cubes(pcn_ondc)
fnc_comp = complement_fnc(cubes_comp, var_list)
fnc_bar = pcn_fnc_comp(fnc_comp, var_list)
print("fnc_bar: " + fnc_bar)
#sorts the cubes of ON set according to their weights
sort_cubes_fnc = cubes_sort(fon, pcn_on, var_list)
print("Sorted cover: ", sort_cubes_fnc)
prime_cover = sort_cubes_fnc
#finding the expanded cube for all the cubes of the function in the sorted manner
for cube in sort_cubes_fnc:
    b_matrix = blocking_matrix(cube, fnc_bar)
    print("Blocking matrix of cube " , cube, "is: " , b_matrix)
    expanded_cube = covering(cube, b_matrix)
    index = prime_cover.index(cube)
    prime_cover[index] = expanded_cube
prime_cover = list(set(prime_cover))
print("Prime cover: ", prime_cover)