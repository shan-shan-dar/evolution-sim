import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

import parameters as prm

import threading


class NeuronUpdaterThread(threading.Thread):
    def __init__(self, neuron):
        threading.Thread.__init__(self)
        self.neuron = neuron

    def run(self):
        self.neuron.calculate_activation()


def update_neurons_parallel(neurons):
    threads = []

    for neuron in neurons:
        thread = NeuronUpdaterThread(neuron)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


class Neuron:
    def __init__(self, brain, neuron_id):
        self.brain = brain

        self.id = neuron_id

        if self.id < prm.num_input_neurons:
            self.type = "input"
        elif self.id < prm.num_input_neurons + prm.num_internal_neurons:
            self.type = "internal"
        else:
            self.type = "output"

        self.activation = 0.0
        self.bias = 0

        self.input_connections = []

    def connect(self):
        for connection in self.brain.connections:
            if connection.sink == self:
                self.input_connections.append(connection)

    def draw_connections(self):
        G = nx.DiGraph()

        for connection in self.input_connections:
            G.add_edge(connection.source.id, connection.sink.id)

        # Draw the graph
        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(
            G,
            pos,
            node_color="lightblue"
            if self.type == "input"
            else ("lightgreen" if self.type == "internal" else "lightcoral"),
            node_size=500,
            label=True,
        )
        nx.draw_networkx_edges(G, pos, edge_color="gray", arrows=True)
        nx.draw_networkx_labels(G, pos)

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

        def calculate_activation_thread():
            weighted_sum = sum(
                connection.weight * connection.source.activation
                for connection in self.input_connections
            )
            self.activation = sigmoid(weighted_sum + self.bias)

        # Create a thread for the calculation
        activation_thread = threading.Thread(target=calculate_activation_thread)

        # Start the thread
        activation_thread.start()

        # Wait for the thread to finish
        activation_thread.join()

    def reset_activation(self):
        self.activation = 0.0

    def update_parallel(self):
        # Create multiple threads
        threads = []
        for neuron in self.input_neurons + self.internal_neurons + self.output_neurons:
            thread = threading.Thread(target=neuron.calculate_activation)
            threads.append(thread)

        # Start all the threads
        for thread in threads:
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()


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

        # make connections
        for i in range(0, len(self.dot.genome.brain), 30):
            source_id = int(self.dot.genome.brain[i : i + 7], 2) % (
                prm.num_input_neurons + prm.num_internal_neurons
            )
            sink_id = (
                int(self.dot.genome.brain[i + 7 : i + 14], 2)
                % (prm.num_internal_neurons + prm.num_output_neurons)
                + prm.num_input_neurons
            )
            weight = (
                int(self.dot.genome.brain[i + 14 : i + 30], 2) / (2**16 - 1)
            ) * 8 - 4

            self.connections.append(Connection(self, source_id, sink_id, weight))

        # connect neruons
        for input_neuron, internal_neuron, output_neuron in zip(
            self.input_neurons, self.internal_neurons, self.output_neurons
        ):
            input_neuron.connect()
            internal_neuron.connect()
            output_neuron.connect()

    def draw_brain(self):
        dot_id = self.dot.id
        G = nx.DiGraph()

        for neuron in self.input_neurons + self.internal_neurons + self.output_neurons:
            G.add_node(neuron)

        for connection in self.connections:
            G.add_edge(connection.source, connection.sink, weight=connection.weight)

        # Define positions for different neuron types
        pos = {}

        # Positioning for input neurons (blue)
        input_x = -1.5
        min_distance = 0.2  # Minimum distance between neighboring neurons
        for neuron in self.input_neurons:
            y = random.uniform(-0.5, 0.5)
            pos[neuron] = np.array([input_x, y])
            input_x += min_distance

        # Positioning for internal neurons (green)
        internal_x = -0.5
        for neuron in self.internal_neurons:
            y = random.uniform(-0.5, 0.5)
            pos[neuron] = np.array([internal_x, y])
            internal_x += min_distance

        # Positioning for output neurons (red)
        output_x = 0.5
        for neuron in self.output_neurons:
            y = random.uniform(-0.5, 0.5)
            pos[neuron] = np.array([output_x, y])
            output_x += min_distance

        # Draw neurons
        neuron_colors = {
            "input": "lightgreen",
            "internal": "lightgrey",
            "output": "lightcoral",
        }
        for neuron in G.nodes:
            node_color = neuron_colors.get(neuron.type, "lightgray")
            nx.draw_networkx_nodes(
                G, pos, nodelist=[neuron], node_color=node_color, node_size=500
            )

            # Add neuron ID as a label inside the circle
            nx.draw_networkx_labels(G, pos, {neuron: neuron.id}, font_size=10)

        # Draw connections
        edge_colors = []
        edge_widths = []
        for source, sink, attrs in G.edges(data=True):
            weight = attrs.get("weight", 0)  # Set weight to 0 if not present
            edge_widths.append(abs(weight) * 0.5)  # Adjust the scaling factor as needed
            edge_colors.append("red" if weight < 0 else "gray")

        edges = G.edges()
        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=edges,
            arrows=True,
            edge_color=edge_colors,
            width=edge_widths,
        )

        # Remove axis labels and ticks
        plt.axis("off")

        # Set the figure title to the dot's ID
        plt.title(f"Dot ID: {dot_id}")

        # Save the figure as an image file with a custom filename based on the dot's ID
        filename = f"dot_{dot_id}.png"
        plt.savefig(filename)

        # Close the figure to release memory resources
        plt.close()

        # Optionally, you can return the filename if you need it for further processing
        return filename

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

    def update_parallel(self):
        update_neurons_parallel(self.input_neurons)
        update_neurons_parallel(self.internal_neurons)
        update_neurons_parallel(self.output_neurons)


def sigmoid(x):
    return 1 / (1 + np.exp(-x))
