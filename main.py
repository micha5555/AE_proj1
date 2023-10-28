
import matplotlib.pyplot as plt
import numpy as np


import settings
from Generation import Generation
from History import History

generation = Generation(None)
history = History()
history.add_generation_to_history(generation)
for i in range(settings.generations):
    generation = generation.next_generation()
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

x_function = np.linspace(settings.min_x, settings.max_x, 100)
y_function = -0.4 * x_function**2 + 4 * x_function + 6
ax2.plot(x_function, y_function, label='-0.4*x^2 + 4*x + 6', color='purple')

ax2.set_xlabel('X-axis')
ax2.set_ylabel('Y-axis (Function Plot)')
ax2.legend(loc='upper right')

ax1.set_title('population size: {p_size}, \ngenerations: {gen}, \ncrossover_probability: {cross_prob} \nmutation_probability: {m_prob}, \nmin_x: {min_x}, \nmax_x: {max_x}'.format(p_size = settings.population_size, gen = settings.generations, cross_prob = settings.crossover_probability, m_prob = settings.mutation_probability, min_x = settings.min_x, max_x = settings.max_x))
ax1.set_xlabel('Generation')
ax1.set_ylabel('Value')
ax1.legend()
plt.tight_layout()
plt.savefig('output.png')
plt.show()