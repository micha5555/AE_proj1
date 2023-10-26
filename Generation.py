class Generation:
    def __init__(self, population):
        self.population = population
        self.minimal_value = self.get_minimal_value(population)
        self.max_value = self.get_max_value(population)
        self.mean_value = self.get_mean_value(population)
        self.best_entity = str(min(population, key=lambda entity: entity.y).x)
        self.best_fitness = str(min(population, key=lambda entity: entity.y).y)
        
    def get_minimal_value(self, population):
        minimal_value = population[0].y
        for entity in population:
            if entity.y < minimal_value:
                minimal_value = entity.y
        return minimal_value
    
    def get_max_value(self, population):
        max_value = population[0].y
        for entity in population:
            if entity.y > max_value:
                max_value = entity.y
        return max_value
    
    def get_mean_value(self, population):
        total = 0
        for entity in population:
            total += entity.y
        return total / len(population)

       

