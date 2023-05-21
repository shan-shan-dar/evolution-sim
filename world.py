import random

from dot import Dot
from genome import Genome
import parameters as prm


class World:
    def __init__(self):

        self.unit = prm.UNIT

        self.width = prm.WORLD_WIDTH
        self.height = prm.WORLD_HEIGHT
        self.color = prm.WORLD_COLOR

        self.mutation_rate = prm.MUTATION_RATE

        self.grid = []
        for i in range(self.width):
            row = []
            for j in range(self.height):
                row.append(0)
            self.grid.append(row)

        self.dots = []

        # stats
        self.time_elapsed = 0
        self.mean_lifespans = []

    def spawn(self, count):
        for i in range(count):
            dot = Dot(
                self,
                random.randint(0, self.width - 1),
                random.randint(0, self.height - 1),
                Genome(
                    "".join(
                        [str(random.randint(0, 1)) for j in range(prm.GENOME_LENGTH)]
                    )
                ),
            )
            self.dots.append(dot)

    def update(self):

        self.time_elapsed += 1

        if self.time_elapsed % prm.lifespan_update_interval == 0:
            mean_lifespan = sum(dot.lifespan for dot in self.dots) / len(self.dots)
            self.mean_lifespans.append(mean_lifespan)

        for dot in list(self.dots):
            dot.update()

        # Clear the grid
        for row in self.grid:
            for i in range(len(row)):
                row[i] = 0

        # Update the grid with dots
        for dot in self.dots:
            self.grid[dot.x][dot.y] = dot
