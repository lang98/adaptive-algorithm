import copy
import math
import random
from typing import Tuple, List


def get_initial_solution(cities: List[int], num_of_routes: int) -> List[List[int]]:
    cities = cities[1:].copy()
    res = [[] for _ in range(num_of_routes)]

    while cities:
        i = random.choice(list(range(num_of_routes)))
        c = random.choice(cities)
        res[i].append(c)
        cities.remove(c)

    print(res)
    return res


def get_neighbor_solution(solution: List[List[int]]) -> List[List[int]]:
    solution = copy.deepcopy(solution)

    def generate_random():
        a = random.choice(list(range(len(solution))))
        b = random.choice(list(range(len(solution))))
        c, d = 0, 0
        if solution[a]:
            c = random.choice(list(range(len(solution[a]))))
        if solution[b]:
            d = random.choice(list(range(len(solution[b]))))
        return a, b, c, d

    # trying to swap two items
    l1, l2, i1, i2 = generate_random()
    solution[l1][i1], solution[l2][i2] = solution[l2][i2], solution[l1][i1]

    # trying to move an item to another
    l1, l2, i1, i2 = generate_random()
    if len(solution[l2]) > 2:
        solution[l1].insert(i1, solution[l2].pop(i2))

    return solution


def calculate_cost(routes: List[List[int]], coord: List[Tuple[int, int]]) -> int:
    def calculate_euclidean_distance(a: Tuple[int, int], b: Tuple[int, int]):
        x_diff = a[0] - b[0]
        y_diff = a[1] - b[1]
        return math.sqrt(x_diff * x_diff + y_diff * y_diff)

    cost = 0
    for route in routes:
        cost += calculate_euclidean_distance(coord[0], coord[route[0]])
        for c in range(1, len(route)):
            cost += calculate_euclidean_distance(coord[route[c - 1]], coord[route[c]])
        cost += calculate_euclidean_distance(coord[route[-1]], coord[0])

    return cost


def simulated_annealing(cities: List[int], num_of_routes: int, coord: List[Tuple[int, int]]) -> Tuple:
    cur_solution = get_initial_solution(cities, num_of_routes)
    cur_cost = calculate_cost(cur_solution, coord)
    best_solution = cur_solution
    best_cost = cur_cost

    T = 1000
    I = 100
    alpha = 0.9

    while T > 1:
        iteration = 0
        while iteration < I:
            neighbor_solution = get_neighbor_solution(cur_solution)
            neighbor_cost = calculate_cost(neighbor_solution, coord)
            delta = neighbor_cost - cur_cost

            if delta < 0:
                cur_solution = neighbor_solution
                cur_cost = neighbor_cost
            else:
                if random.random() < math.exp(- delta / T):
                    cur_solution = neighbor_solution
                    cur_cost = neighbor_cost

            iteration += 1
        T *= alpha
        if cur_cost < best_cost:
            print(best_cost)
            best_cost = cur_cost
            best_solution = cur_solution

    return best_cost, best_solution


def read_file(name: str) -> Tuple:
    d = 0  # number of cities, including depot
    c = 0  # capacity of each vehicle
    v = 0  # min no of vehicles/routes
    coord = []  # coordinates of cities
    dem = []  # demands of cities
    dep = []  # index of depots

    reading_node = False
    reading_demand = False
    reading_depot = False
    file = open(name, 'r')
    for line in file:
        data = line.split()
        k = data[0]

        if '_SECTION' not in str(data):
            if reading_node:
                coord.append((int(data[1]), int(data[2])))
            elif reading_demand:
                dem.append(int(data[1]))
            elif reading_depot and data[0] not in ['-1', 'EOF']:
                dep.append(int(data[0]))

        if k == 'NAME':
            name = data[2]
            v = int(name.split('-')[-1][-1])
        elif k == 'DIMENSION':  # number of cities and depot
            d = int(data[2])
        elif k == 'CAPACITY':  # capacity of each vehicle
            c = int(data[2])
        elif k == 'DEPOT_SECTION':  # list of all depot nodes
            reading_depot = True
            reading_demand = False
            reading_node = False
        elif k == 'NODE_COORD_SECTION':
            reading_node = True
            reading_demand = False
            reading_depot = False
        elif k == 'DEMAND_SECTION':
            reading_demand = True
            reading_node = False
            reading_depot = False

    return d, c, v, coord, dem, dep


dim, cap, num_veh, coordinates, demands, depots = read_file('A-n39-k6.vrp')
list_of_cities = list(range(dim))

simulated_annealing(list_of_cities, num_veh, coordinates)

# get_neighbor_solution([[1, 2, 3], [4, 5, 6]])
