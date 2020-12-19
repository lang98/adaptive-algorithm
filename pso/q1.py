import random
import numpy as np
import matplotlib.pyplot as plt


class Particle:
    def __init__(self, w=0.792, c1=1.4944, c2=1.4944, constriction=1):
        self.position = np.array([
            random.uniform(-5, 5),
            random.uniform(-5, 5),
        ])
        self.velocity = np.array([
            random.uniform(-1, 1),
            random.uniform(-1, 1),
        ])

        self.w = w
        self.c1 = c2
        self.c2 = c2
        self.constriction = constriction

        self.best_fitness = float('inf')
        self.best = self.position

    
    def fitness(self):
        def camelback(x, y):
            a = (4 - 2.1 * x ** 2 + (x ** 4) / 3.) * x ** 2
            b = x * y
            c = (-4 + 4 * y ** 2) * y ** 2
            return a + b + c
        return camelback(self.position[0], self.position[1])

    
    def update_pbest(self):
        if self.fitness() < self.best_fitness:
            self.best_fitness = self.fitness()
            self.best = self.position

    def update_velocity(self, gbest):
        self.velocity = self.w * self.velocity + \
            self.c1 * random.random() * (self.best - self.position) + \
            self.c2 * random.random() * (gbest - self.position)
        self.velocity *= self.constriction

    def update_position(self):
        res = self.position + self.velocity
        self.position = res
        if res[0] > 5:
            self.position[0] = 5
            self.position[1] = res[1]
        elif res[0] < -5:
            self.position[0] = -5
            self.position[1] = res[1]
        elif res[1] > 5:
            self.position[0] = res[0]
            self.position[1] = 5
        elif res[1] < -5:
            self.position[0] = res[0]
            self.position[1] = -5


def pso(num_particles=50, iterations=10):
    # Inertia Weight
    # particles = [Particle(w=0.8, c1=2, c2=2.1) for _ in range(num_particles)]
    # Constriction Factor
    # particles = [Particle(w=0.8, c1=2.05, c2=2.05, constriction=0.729) for _ in range(num_particles)]
    # Guaranteed Convergence PSO
    particles = [Particle()e for _ in range(num_particles)]

    gbest = None
    gbest_fitness = float('inf')

    ## plt
    avg_fitnesses = []
    best_fitnesses = []

    for i in range(iterations):
        for p in particles:
            fitness = p.fitness()
            p.update_pbest()
            if fitness < gbest_fitness:
                gbest = p.position
                gbest_fitness = fitness

        for p in particles:
            p.update_velocity(gbest)
            p.update_position()
        
        avg = np.mean(list(map(lambda p: p.fitness(), particles)))
        
        avg_fitnesses.append(avg)
        best_fitnesses.append(gbest_fitness)

        print(i, gbest, gbest_fitness)

    x_axis = np.arange(0, iterations, step=1)

    plt.subplot(211)
    plt.plot(x_axis, avg_fitnesses, label='Average fitness')
    plt.xlabel('iteration')
    plt.ylabel('z')
    plt.legend()

    plt.subplot(212)
    plt.plot(x_axis, best_fitnesses, label='Best fitness')
    plt.xlabel('iteration')
    plt.ylabel('z')
    plt.legend()
    plt.show()

pso()