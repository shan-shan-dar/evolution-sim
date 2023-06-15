import random
import math
from scipy.special import erfinv

from genome import Genome
from brain import Brain
import parameters as prm


class Dot:
    id = 0

    def __init__(self, world, x, y, genome):
        self.alive = True

        self.id = Dot.id
        Dot.id += 1

        # environment
        self.world = world

        # position in world
        self.x = x
        self.y = y

        # genome
        self.genome = genome

        # brain
        self.brain = Brain(self)
        # self.brain.draw_brain()

        # gene independent properties
        self.age = 0
        self.size = 1
        self.speed = 0.5
        self.radius = 10
        self.reproduction_rate = self.set_reproduction_rate()

        # gene dependent properties
        self.color = self.set_color()
        self.lifespan = self.set_lifespan()

    def set_lifespan(self):
        if not self.world.dots:
            return prm.INITIAL_LIFESPAN

        value = value = int(self.genome.lifespan, 2) / 63
        EPSILON = 1e-6
        value = min(value, 1 - EPSILON)  # ensure that the value is less than 1
        value = max(value, EPSILON)

        mean = sum(dot.lifespan for dot in self.world.dots) / len(self.world.dots)

        stdev = 50

        quantile = math.sqrt(2) * erfinv(value * 2 - 1)
        return round(random.gauss(mean, stdev * quantile))

    def set_reproduction_rate(self):
        EPSILON = 1e-6
        while True:
            rate = random.gauss(
                prm.MEAN_REPRODUCTION_RATE, prm.REPRODUCTION_RATE_STDDEV
            )
            if rate > 1 - EPSILON:
                return 1 - EPSILON

            elif rate < EPSILON:
                return EPSILON

            else:
                return rate

    # Convert decimal number to RGB value
    def set_color(self):
        genome_len = len(self.genome.genome)
        part_len = genome_len // 3

        # Convert each part of the genome to a decimal value
        part1 = int(self.genome.genome[:part_len], 2)
        part2 = int(self.genome.genome[part_len : 2 * part_len], 2)
        part3 = int(self.genome.genome[2 * part_len :], 2)

        # Scale the values to the range of 0-255
        r = int((part1 / (2**part_len - 1)) * 255)
        g = int((part2 / (2**part_len - 1)) * 255)
        b = int((part3 / (2**part_len - 1)) * 255)

        return (r, g, b)

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy

        if (
            0 <= new_x < self.world.width
            and 0 <= new_y < self.world.height
            and not isinstance(self.world.grid[new_x][new_y], Dot)
        ):
            # move to next tile
            self.x = new_x
            self.y = new_y

    def get_population_density(self, radius=None):
        if radius == None:
            radius = self.radius

        # count the number of dots in the sense radius
        count = 0
        for dx in range(int(-radius), int(radius) + 1):
            for dy in range(int(-radius), int(radius) + 1):
                if (
                    (dx == 0 and dy == 0)
                    or self.x + dx < 0
                    or self.x + dx >= self.world.width
                    or self.y + dy < 0
                    or self.y + dy >= self.world.height
                ):
                    continue  # don't count this dot or out-of-bounds dots
                if isinstance(self.world.grid[self.x + dx][self.y + dy], Dot):
                    count += 1

        # return the population density (normalized by the area of the sense radius)
        return count / ((2 * radius + 1) ** 2 - 1)

    def get_x_direction(self):
        if self.x > self.last_x:
            return 1
        elif self.x < self.last_x:
            return -1
        else:
            return 0

    def get_y_direction(self):
        if self.y > self.last_y:
            return 1
        elif self.y < self.last_y:
            return -1
        else:
            return 0

    def reproduce(self):
        empty_squares = []
        if prm.RANDOM_OFFSPRING_POSITION:
            for x in range(self.world.width):
                for y in range(self.world.height):
                    if not isinstance(self.world.grid[x][y], Dot):
                        empty_squares.append((x, y))
        else:
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx == 0 and dy == 0:
                        continue
                    x = self.x + dx
                    y = self.y + dy
                    if (0 <= x < self.world.width) and (0 <= y < self.world.height):
                        if not isinstance(self.world.grid[x][y], Dot):
                            empty_squares.append((x, y))

        if empty_squares and self.get_population_density(10) < 0.0075:
            child_x, child_y = random.choice(empty_squares)
            child = Dot(
                self.world,
                child_x,
                child_y,
                self.genome.mutate(self.world.mutation_rate),
            )

            self.world.dots.append(child)

    def die(self):
        self.world.dots.remove(self)

    def update(self):
        self.age += 1
        self.last_x = self.x
        self.last_y = self.y

        self.brain.update_parallel()
        # Get output activations from the dot's brain
        output_activations = self.brain.get_output_activations()

        prm.selection_pressures(self)

        # movement
        movement_threshold = 0.3

        if output_activations[0] <= -movement_threshold:
            dx = -1
        elif output_activations[0] >= movement_threshold:
            dx = 1
        else:
            dx = 0

        if output_activations[1] <= -movement_threshold:
            dy = -1
        elif output_activations[1] >= movement_threshold:
            dy = 1
        else:
            dy = 0

        # radius sensing
        self.radius = abs(output_activations[2]) * 150

        self.move(dx, dy)

        if random.random() < self.reproduction_rate:
            self.reproduce()
