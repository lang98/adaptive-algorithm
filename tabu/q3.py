import itertools as it
from typing import List, Dict

import numpy as np

# global consts
flow = np.genfromtxt('Flow.csv', delimiter=',', dtype='int')
distance = np.genfromtxt('Distance.csv', delimiter=',', dtype='int')


def get_cost(permutation: List):
    temp1 = np.copy(flow)
    for i, v in enumerate(flow):
        temp1[i, :] = flow[permutation[i] - 1, :]

    temp2 = np.copy(temp1)
    for i, v in enumerate(temp1):
        temp2[:, i] = temp1[:, permutation[i] - 1]

    return sum(np.diag(temp2.dot(distance)))


def get_neighbor_move(move: List, a: int, b: int):
    next_move = move.copy()
    next_move[a], next_move[b] = next_move[b], next_move[a]
    return next_move


def decrement_tabu(t: Dict):
    for k in t:
        if t[k] > 0:
            t[k] -= 1


"""
Main
"""
MAX_I = 1000

p = list(range(20))
# random.shuffle(p)
p_opt = [18, 14, 10, 3, 9, 4, 2, 12, 11, 16, 19, 15, 20, 8, 13, 17, 5, 7, 1, 6]

tabu = {}

init_cost = get_cost(p)
opti_cost = get_cost(p_opt)
print('init: ', init_cost)
print('optimal: ', opti_cost)

cost = init_cost
prev_cost = cost
min_cost = cost
min_p = p

for _ in range(MAX_I):
    decrement_tabu(tabu)
    combinations = list(it.combinations(p, 2))
    d = {}

    for i, v in enumerate(combinations):
        perm = get_neighbor_move(p, v[0], v[1])
        cost = get_cost(perm)
        d[v] = cost

    minimum = min(d, key=d.get)

    # if minimum > min_cost: # aspiration best solution so far
    while minimum in tabu and tabu[minimum] > 0:
        del d[minimum]
        minimum = min(d, key=d.get)

    # tabu[minimum] = 10
    # tabu[minimum] = np.random.randint(10, 50)  # rand tabu list size
    tabu[minimum] = tabu.get(minimum, 0) + 1  # frequency based tabu

    p = get_neighbor_move(p, minimum[0], minimum[1])
    cost = get_cost(p)

    if cost < min_cost:
        min_cost = cost
        min_p = p
        print('Better solution', min_cost, min_p)
