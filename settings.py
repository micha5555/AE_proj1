import json

settings_file = open('settings.json')
settings = json.load(settings_file)

fitness_function = settings['fitness_function']
population_size = settings['population_size']
generations = settings['generations']
mutation_probability = settings['mutation_probability']
min_x = settings['min_x']
max_x = settings['max_x']