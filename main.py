'''


'''

import random
import matplotlib.pyplot as plt
import numpy as np

import settings
from Entity import Entity
from Generation import Generation
from History import History

def initialize_population():
    population = []
    for i in range(settings.population_size):
        entity_x = random.randint(settings.min_x, settings.max_x)
        population.append(Entity(entity_x))
    calculate_fitness(population)
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
        children.append(child1)
        children.append(child2)
    calculate_fitness(children)
    return children

def mutate(children):
    for child in children:
        if random.random() < settings.mutation_probability:
            can_mutate = True
            while can_mutate:
                mutation_point = random.randint(0, len(child.binary)-1)
                child.change_x(int(child.binary[:mutation_point] + str(random.randint(0, 1)) + child.binary[mutation_point+1:], 2))
                if (child.x > settings.max_x) or (child.x < settings.min_x):
                    can_mutate = True
                else:
                    can_mutate = False
    calculate_fitness(children)
    return children

generation = Generation(initialize_population())
history = History()
history.add_generation_to_history(generation)
for i in range(settings.generations):
    parents = select_parents(generation.population)
    children = crossover(parents)
    children = mutate(children)
    generation = Generation(children)
    print("Generation: " + str(i+1) + " | Best entity: " + generation.best_entity + " | Best fitness: " + generation.best_fitness)
    history.add_generation_to_history(generation)
    
x_points = []
minimal_values_points = []
max_values_points = []
mean_values_points = []


for i in range(settings.generations+1):
    x_points.append(i)
    minimal_values_points.append(history.minimal_values[i])
    max_values_points.append(history.max_values[i])
    mean_values_points.append(history.mean_values[i])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

ax1.scatter(x_points, minimal_values_points, label='Minimal Values', color='blue')
ax1.scatter(x_points, max_values_points, label='Max Values', color='green')
ax1.scatter(x_points, mean_values_points, label='Mean Values', color='red')

# Plot the second set of data (function) on the second subplot (ax2)
x_function = np.linspace(settings.min_x, settings.max_x, 100)
y_function = -0.4 * x_function**2 + 4 * x_function + 6
ax2.plot(x_function, y_function, label='-0.4*x^2 + 4*x + 6', color='purple')

ax2.set_xlabel('X-axis')
ax2.set_ylabel('Y-axis (Function Plot)')
ax2.legend(loc='upper right')

ax1.set_xlabel('Generation')
ax1.set_ylabel('Value')
ax1.legend()
plt.tight_layout()
plt.savefig('my_plot.png')
plt.show()