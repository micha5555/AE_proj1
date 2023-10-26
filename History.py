class History:
    def __init__(self):
        self.minimal_values = []
        self.max_values = []
        self.mean_values = []
    
    def add_generation_to_history(self, generation):
        self.minimal_values.append(generation.minimal_value)
        self.max_values.append(generation.max_value)
        self.mean_values.append(generation.mean_value)