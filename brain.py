import random
import numpy as np


import parameters as prm


class Neuron:
    def __init__(self, brain, neuron_id):
        self.brain = brain

        self.id = neuron_id

        if self.id < len(self.brain.input_neurons):
            self.type = "input"
        elif self.id < len(self.brain.input_neurons) + len(self.brain.internal_neurons):
            self.type = "internal"
        else:
            self.type = "output"

        self.activation = 0.0
        self.bias = 0

        self.input_connections = []

        for connection in self.brain.connections:
            if connection.sink == self:
                self.input_connections.append(connection)

    def calculate_activation(self):
        if self.id == 0:
            self.activation = self.brain.dot.x / prm.WORLD_WIDTH

        elif self.id == 1:
            self.activation = self.brain.dot.y / prm.WORLD_WIDTH

        elif self.id == 2:
            self.activation = self.brain.dot.get_x_direction()

        elif self.id == 3:
            self.activation = self.brain.dot.get_y_direction()

        elif self.id == 4:
            self.activation = self.brain.dot.get_population_density(
                self.brain.dot.radius
            )

        else:
            weighted_sum = sum(
                connection.weight * connection.source.activation
                for connection in self.input_connections
            )
            self.activation = sigmoid(weighted_sum + self.bias)

    def reset_activation(self):
        self.activation = 0.0


class Connection:
    def __init__(self, brain, source_id, sink_id, weight):
        self.brain = brain

        self.source = None
        self.sink = None
        self.weight = weight

        # Find the source neuron in the input or internal neuron lists
        for neuron in self.brain.input_neurons + self.brain.internal_neurons:
            if neuron.id == source_id:
                self.source = neuron
                break

        # Find the sink neuron in the internal or output neuron lists
        for neuron in self.brain.internal_neurons + self.brain.output_neurons:
            if neuron.id == sink_id:
                self.sink = neuron
                break


class Brain:
    def __init__(self, dot):
        self.dot = dot

        self.input_neurons = []
        self.internal_neurons = []
        self.output_neurons = []

        self.connections = []

        for i in range(0, len(self.dot.genome.brain), 30):
            source_id = int(self.dot.genome.brain[i : i + 7], 2)
            sink_id = int(self.dot.genome.brain[i + 7 : i + 14], 2)
            weight = int(self.dot.genome.brain[i + 14 : i + 30], 2) / 8500
            self.connections.append(Connection(self, source_id, sink_id, weight))

        # Assign IDs to input neurons
        for i in range(prm.num_input_neurons):
            self.input_neurons.append(Neuron(self, i))

        # Assign IDs to internal neurons
        for i in range(
            prm.num_input_neurons, prm.num_input_neurons + prm.num_internal_neurons
        ):
            self.internal_neurons.append(Neuron(self, i))

        # Assign IDs to output neurons
        for i in range(
            prm.num_input_neurons + prm.num_internal_neurons, prm.num_neurons
        ):
            self.output_neurons.append(Neuron(self, i))

    def get_output_activations(self):
        output_activations = []
        for neuron in self.output_neurons:
            output_activations.append(neuron.activation)
        return output_activations

    def update(self):
        for neuron in self.input_neurons:
            neuron.calculate_activation()

        for neuron in self.internal_neurons:
            neuron.calculate_activation()

        for neuron in self.output_neurons:
            neuron.calculate_activation()


def sigmoid(x):
    return 1 / (1 + np.exp(-x))
