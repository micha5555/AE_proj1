import random

import settings
from Entity import Entity

class Generation:
    def __init__(self, population):
        if population is None:
            self.population = Generation.initialize_population()
        else:
            self.population = population
        self.minimal_value = self.get_minimal_value()
        self.max_value = self.get_max_value()
        self.mean_value = self.get_mean_value()
    
    def initialize_population():
        population = []
        for i in range(settings.population_size):
            entity_x = random.randint(settings.min_x, settings.max_x)
            population.append(Entity(entity_x))
        Generation.calculate_fitness(population)
        return population

    def calculate_fitness(population):
        total = 0
        min_value_of_y = population[0].y
        for entity in population:
            if entity.y < min_value_of_y:
                min_value_of_y = entity.y
        abs_value_of_min_value_of_y = abs(min_value_of_y)+1
        for entity in population:
            total += entity.y + abs_value_of_min_value_of_y
        for entity in population:
            entity.set_percent_score((entity.y+abs_value_of_min_value_of_y) / total)
    
    def select_parents(population):
        parents = []
        for _ in range(len(population)):
            parents.append(random.choices(population, weights=[entity.percent_score for entity in population])[0])
        return parents

    def crossover(parents):
        children = []
        for i in range(0, len(parents), 2):
            parent1 = parents[i]
            parent2 = parents[i+1]
            parent_1_offset = 0
            parent_2_offset = 0
            if parent1.binary[0] == '-':
                parent_1_offset = 1
            if parent2.binary[0] == '-':
                parent_2_offset = 1
            if parent_1_offset == 1 and parent_2_offset == 1:
                parent_1_offset = 0
                parent_2_offset = 0
            if parent_2_offset == 1:
                crossover_point = random.randint(0, len(parent2.binary))
            else:
                crossover_point = random.randint(0, len(parent1.binary))
            child1 = Entity(int(parent1.binary[:crossover_point+parent_1_offset] + parent2.binary[crossover_point+parent_2_offset:], 2))
            child2 = Entity(int(parent2.binary[:crossover_point+parent_2_offset] + parent1.binary[crossover_point+parent_1_offset:], 2))
            if(child1.x > settings.max_x) or (child1.x < settings.min_x) or (child2.x > settings.max_x) or (child2.x < settings.min_x):
                i = i - 2
                continue
            if random.random() < settings.crossover_probability:
                children.append(child1)
                children.append(child2)
            else:
                children.append(parent1)
                children.append(parent2)
        Generation.calculate_fitness(children)
        return children

    def mutate(children):
        for child in children:
            if random.random() < settings.mutation_probability:
                can_mutate = True
                while can_mutate:
                    mutation_point = random.randint(0, len(child.binary)-1)
                    digit_after_mutate = '0' if child.binary[mutation_point] == '1' else '1'
                    child.change_x(int(child.binary[:mutation_point] + digit_after_mutate + child.binary[mutation_point+1:], 2))
                    if (child.x > settings.max_x) or (child.x < settings.min_x):
                        can_mutate = True
                    else:
                        can_mutate = False
        Generation.calculate_fitness(children)
        return children

    def next_generation(self):
        parents = Generation.select_parents(self.population)
        children = Generation.crossover(parents)
        children = Generation.mutate(children)
        return Generation(children)

    def get_minimal_value(self):
        minimal_value = self.population[0].y
        for entity in self.population:
            if entity.y < minimal_value:
                minimal_value = entity.y
        return minimal_value
    
    def get_max_value(self):
        max_value = self.population[0].y
        for entity in self.population:
            if entity.y > max_value:
                max_value = entity.y
        return max_value
    
    def get_mean_value(self):
        total = 0
        for entity in self.population:
            total += entity.y
        return total / len(self.population)