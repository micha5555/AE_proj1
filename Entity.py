import settings

fitness_function = settings.fitness_function

class Entity:
    def __init__(self, x):
        self.x = x
        self.y = eval(fitness_function)
        self.binary = format(x, 'b')
        
    def change_x(self, new_x):
        self.x = new_x
        x = new_x
        self.y = eval(fitness_function)
        self.binary = format(new_x, 'b')

    def set_percent_score(self, percent_score):
        self.percent_score = percent_score


