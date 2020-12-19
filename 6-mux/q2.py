import math
import random

from evaluate import Evaluator


class Program:
    def __init__(self, order=6):
        self.depth = 0
        self.max_depth = 0
        self.order = order

        if order == 6:
            self.depth = 3
            self.max_depth = 5
        elif order == 11:
            self.depth = 3
            self.max_depth = 8
        elif order == 16:
            self.depth = 5
            self.max_depth = 10

        self.tree = self.generate_random_tree(self.depth)

    def generate_random_tree(self, depth):
        from if_node import IfNode
        from and_node import AndNode
        from not_node import NotNode
        from or_node import OrNode
        r = random.randint(0, 3)
        m = {
            0: AndNode(self.order),
            1: OrNode(self.order),
            2: NotNode(self.order),
            3: IfNode(self.order)
        }
        root = m[r]
        root.build(depth - 1)
        return root

    def mutate(self):
        tree = self.tree.clone()
        point = random.choice(tree.nonT_list() + tree.T_list())
        new_tree = self.generate_random_tree(random.randint(0, self.depth))
        tree.swap_child(point, new_tree)
        self.tree = tree

    def crossover(self, other):
        parent1 = self.tree.clone()
        parent2 = other.tree.clone()
        cross1 = random.choice(parent1.nonT_list())
        cross2 = random.choice(parent2.nonT_list())

        parent1.swap_child(cross1, cross2)
        parent2.swap_child(cross2, cross1)

        self.tree = parent1
        other.tree = parent2

    def fitness(self):
        total = math.pow(2, self.order)
        fitness = 0
        for i in range(int(total)):
            evaluator = Evaluator(self.order, i)
            output = self.tree.value(evaluator)
            expected = evaluator.expected()
            if output == expected:
                fitness += 1
        return fitness


####################################
# main
####################################

def tournament_select(population) -> Program:
    sample = random.choices(population, k=50)
    return max(sample, key=lambda x: x.fitness())


def evolve(order=6, pop_size=50, iterations=100, p_crossover=0.6, p_mutation=0.2):
    population = [Program(order=order) for _ in range(pop_size)]
    best = None
    best_fitness = -float('inf')

    for it in range(iterations):
        new_population = []
        sorted_pop = sorted(population, key=lambda x: x.fitness())
        new_population.append(sorted_pop[-1])
        new_population.append(sorted_pop[-2])

        while len(new_population) < pop_size:
            parent1 = tournament_select(population)
            parent2 = tournament_select(population)
            if random.random() < p_crossover:
                parent1.crossover(parent2)
                for o in [parent1, parent2]:
                    if random.random() < p_mutation:
                        o.mutate()
            new_population += [parent1, parent2]

        population = new_population
        print('lol')
        for p in population:
            f = p.fitness()
            if f == math.pow(2, order):
                print(it, '############# found the best solution', p.tree.show())
                return
            if f > best_fitness:
                best = p
                best_fitness = f
                print(it, '############# better', p.tree.show())


evolve(order=6)
