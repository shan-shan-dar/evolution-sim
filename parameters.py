import random

UNIT = 2

WORLD_WIDTH = 300
WORLD_HEIGHT = 300
WORLD_COLOR = (0, 0, 0)

lifespan_update_interval = 500

STARTING_POPULATION = 300

FPS = 60

INITIAL_LIFESPAN = 500

MUTATION_RATE = 0.02

MEAN_REPRODUCTION_RATE = 0.0075
REPRODUCTION_RATE_STDDEV = 0.01
RANDOM_OFFSPRING_POSITION = True

GENOME_LENGTH = 30

FAST_FORWARD_RATE = 100

num_input_neurons = 5
num_internal_neurons = 2
num_output_neurons = 3

num_neurons = num_input_neurons + num_internal_neurons + num_output_neurons


def selection_pressures(dot):
    # natural death
    if dot.age >= dot.lifespan:
        dot.die()
        return "Age"

    # overcrowding
    density = dot.get_population_density(10)
    if density > 0.0075:
        dot.die()
        return "Overcrowding"

    # right quarter
    if random.random() < dot.x / (WORLD_WIDTH * 100):
        dot.die()
        return "right"

    # redness
    redness = dot.color[0]
    if random.random() < redness / 10000:
        dot.die()
        return "Redness"