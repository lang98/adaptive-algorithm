import math
import random
import matplotlib.pyplot as plt

cities = [
    (1150.0, 1760.0),
    (630.0, 1660.0),
    (40.0, 2090.0),
    (750.0, 1100.0),
    (750.0, 2030.0),
    (1030.0, 2070.0),
    (1650.0, 650.0),
    (1490.0, 1630.0),
    (790.0, 2260.0),
    (710.0, 1310.0),
    (840.0, 550.0),
    (1170.0, 2300.0),
    (970.0, 1340.0),
    (510.0, 700.0),
    (750.0, 900.0),
    (1280.0, 1200.0),
    (230.0, 590.0),
    (460.0, 860.0),
    (1040.0, 950.0),
    (590.0, 1390.0),
    (830.0, 1770.0),
    (490.0, 500.0),
    (1840.0, 1240.0),
    (1260.0, 1500.0),
    (1280.0, 790.0),
    (490.0, 2130.0),
    (1460.0, 1420.0),
    (1260.0, 1910.0),
    (360.0, 1980.0)
]

distances = [0 for _ in enumerate(cities) for _ in enumerate(cities)]
for i, from_city in enumerate(cities):
    for j, to_city in enumerate(cities):
        d = math.sqrt((from_city[0]-to_city[0])**2 + (from_city[1]-to_city[1])**2)
        distances[i][j] = d
        distances[j][i] = d


pheromones = [0 if i == j else 500 for i, _ in enumerate(cities) for j, _ in enumerate(cities)]


def generate_solution(alpha, beta, q0):        
    start_city = random.randint(0, 28)
    sol = [start_city]

    cur_city = start_city
    unvisted = set(range(29)) - set(sol)
    while unvisted:
        denominator = 0
        next_city = -1
        neighbours = []
        if random.uniform(0, 1) < q0: # greedy
            for i in list(unvisted):
                ph = pheromones[i][cur_city]
                d = distances[i][cur_city]
                neighbours.append((i, (ph**alpha)/(d**beta)))
            next_city = max(neighbours, key=lambda x: x[1])[0]
        else: # probability-based
            for i in list(unvisted):
                ph = pheromones[i][cur_city]
                d = distances[i][cur_city]
                denominator += (ph**alpha)/(d**beta)
                neighbours.append((i, denominator))
            for i, prob in neighbours:
                if prob >= random.uniform(0, denominator):
                    next_city = i
                    break
        unvisted.remove(next_city)
        sol.append(next_city)
        cur_city = next_city
    return sol


def calculate_cost(solution):
    return sum(distances[v][solution[i+1]] for i, v in enumerate(solution[:-1]))


def update_pheromones(solution, cost, Q):
    for i, v in enumerate(solution[:-1]):
        pheromones[v][solution[i+1]] += Q/cost


def evaporate(rho):
    for i in range(29):
        for j in range(29):
            pheromones[i][j] *= 1-rho
            pheromones[j][i] *= 1-rho


def aco(num_ants=50, alpha=5, beta=20, q0=0.3, rho=0.15, online=True, iterations=200):
    best_cost = float('inf')
    best_solution = []
    best_for_plot = []
    for _ in range(iterations):
        for ant in range(num_ants):
            solution = generate_solution(alpha, beta, q0)
            cost = calculate_cost(solution)
            if cost < best_cost:
                print(best_cost)
                best_cost = cost
                best_solution = solution[:]
            if online:
                update_pheromones(solution, cost, 12000)
            evaporate(rho)
        if not online:
            update_pheromones(best_solution, best_cost, 12000)
        best_for_plot.append(best_cost)
    return (range(iterations), best_for_plot)


### main

# ## Change pheromone constant
# fig, axs = plt.subplots(3, sharex=True)
# for i, rho in enumerate([0.05, 0.15, 0.25]):
#     x, y = aco(rho=rho)
#     axs[i].plot(x, y)
#     axs[i].set_title(f'Pheromone persistence = {rho}')
# plt.show()

# ## Change state transition control
# fig, axs = plt.subplots(3, sharex=True)
# for i, q0 in enumerate([0.1, 0.3, 0.5]):
#     x, y = aco(q0=q0)
#     axs[i].plot(x, y)
#     axs[i].set_title(f'State transition = {q0}')
# plt.show()

# ## Change population size
# fig, axs = plt.subplots(2, sharex=True)
# for i, num_ants in enumerate([30, 100]):
#     x, y = aco(num_ants=num_ants)
#     axs[i].plot(x, y)
#     axs[i].set_title(f'Number of ants = {num_ants}')
# plt.show()

## Change online
fig, axs = plt.subplots(2, sharex=True)
for i, online in enumerate([True, False]):
    x, y = aco(online=online)
    axs[i].plot(x, y)
    axs[i].set_title(f'Online update = {online}')
plt.show()