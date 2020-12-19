# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 10:59:15 2016

@author: akshaybudhkar
Best so far: {'instance': [17, 13, 9, 2, 8, 3, 1, 11, 10, 15, 18, 14, 19, 7, 12, 16, 4, 6, 0, 5], 'cost': 2570, 'iterations': 350}
"""
import csv
import random

import matplotlib.pyplot as plt


# Returns a column of a matrix as a list
def get_column(index, matrix):
    return [row[index] for row in matrix]


# Uses the standard way to calculate cost in a QAP problem
def calculate_cost(instance, flow_arr, distance_arr):
    permutation_flow = [[0 for i in range(20)] for j in range(20)]
    permut_flow_permut = [[0 for i in range(20)] for j in range(20)]
    cost = 0

    # PF
    for i in range(len(instance)):
        permutation_flow[i] = flow_arr[instance[i]]

    # PFP
    for i in range(len(instance)):
        flow_col = get_column(instance[i], permutation_flow)

        for j in range(len(permut_flow_permut)):
            permut_flow_permut[j][i] = flow_col[j]

    # PFP * D
    for i in range(len(distance_arr)):
        row_cost = 0
        for j in range(len(distance_arr[0])):
            row_cost += permut_flow_permut[i][j] * distance_arr[i][j]

        cost += row_cost

    return cost


""" 
Gives the most optimal neighbor in a neighborhood
Takes into account tabued options and aspirations
"""


def get_most_optimal_neighbor(instance, flow_arr, distance_arr, tabu_matrix, tabu_size, best):
    best_cost = float("inf")
    best_instance = None

    # Check for every possible switch
    for i in range(len(instance)):
        # limit = random.randint(1, 20)
        # change to range(limit) to limit the neighbourhood
        for j in range(len(instance)):
            # Don't switch with itself
            if j > i:
                new_instance = instance[:]
                new_instance[i], new_instance[j] = new_instance[j], new_instance[i]
                new_cost = calculate_cost(new_instance, flow_arr, distance_arr)

                # Check if better than best so far and if not tabued (taking into account aspiration)
                if new_cost < best_cost:
                    if (tabu_matrix[new_instance[i]][i] == 0 and tabu_matrix[new_instance[j]][j] == 0) \
                            or (new_instance == best and tabu_matrix[new_instance[i]][i] < 3 and
                                tabu_matrix[new_instance[j]][j] < 3):
                        best_cost = new_cost
                        best_instance = new_instance
                        tabu_matrix[new_instance[j]][j] = tabu_size
                        tabu_matrix[new_instance[i]][i] = tabu_size

    print
    best_cost
    return best_instance


# Decrement elements tabued in a matrix
def decrement_tabu(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] > 0:
                matrix[i][j] -= 1
    return matrix


# Implements standard Tabu search to get the most optimal solution
def tabu_search(instance, flow_arr, distance_arr, tabu_matrix):
    current = instance
    current_cost = calculate_cost(current, flow_arr, distance_arr)
    best_cost = current_cost
    iterations = 0
    tabu_size = 8
    best = instance
    costs = []  # For plottinh purposes

    # Waiting condition = if we reach optimal or we ~1k iterations
    while current_cost > 2570 and iterations < 1000:
        current = get_most_optimal_neighbor(current, flow_arr, distance_arr, tabu_matrix, tabu_size, best)
        current_cost = calculate_cost(current, flow_arr, distance_arr)

        tabu_matrix = decrement_tabu(tabu_matrix)

        # Dynamic tabu tenure
        if iterations % 50 == 0:
            tabu_size = random.randint(1, 20)

        if current_cost < best_cost:
            # Diversification
            if iterations > 250 or current_cost < 2600:
                best_cost = current_cost
                best = current
            else:
                best = []

        iterations += 1
        costs.append(current_cost)

    plt.plot(costs)
    plt.ylim([2000, 3500])
    plt.plot((0, 1000), (2570, 2570))  # Ideal
    plt.show()

    # Return the best ever
    return {'cost': best_cost,
            'iterations': iterations,
            'instance': best}


# Initial flow and distance arrays setup
flow_file = open('Flow.csv', 'r')
distance_file = open('Distance.csv', 'r')

flow_arr = []
distance_arr = []

flow_reader = csv.reader(flow_file)
distance_reader = csv.reader(distance_file)

for row in flow_reader:
    flow_arr.append([int(x) for x in row])

for row in distance_reader:
    distance_arr.append([int(x) for x in row])

""" 
Initial tabu structure
Defined as departments as rows and locations as columns (a 2D Dimensional Array)
"""
tabu_matrix = [[0 for i in range(20)] for j in range(20)]

init_soln = [i for i in range(20)]

# Shuffle for random initial solution
random.shuffle(init_soln)

print(tabu_search(init_soln, flow_arr, distance_arr, tabu_matrix))
print("Initial: " + str(init_soln))
