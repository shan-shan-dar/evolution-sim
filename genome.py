import random

from brain import Connection


class Genome:
    def __init__(self, genome):
        self.genome = genome

        self.init_attributes()

    def init_attributes(self):
        self.lifespan = self.genome[0:6]
        self.brain = self.genome[6:]

    def mutate(self, mutation_rate):
        mutated_genome = Genome("")
        for bit in self.genome:
            if random.random() < mutation_rate:
                mutated_genome.genome += "0" if bit == "1" else "1"
            else:
                mutated_genome.genome += bit
        mutated_genome.init_attributes()
        return mutated_genome
