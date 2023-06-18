from world import World
from dot import Dot
import parameters as prm
import pandas as pd
import keyboard

print("Initiated")

world = World()

paused = False
stop_simulation = False

simulation_data = {}
dot_static_info = {}

world.spawn(prm.STARTING_POPULATION)

frame = 0  # Initialize frame counter

while not stop_simulation:
    if not paused:
        world.update()

    # Store dot information
    simulation_data[frame] = {}  # Create a new frame entry in dot_data
    for dot in world.dots:
        simulation_data[frame][dot.id] = {
            "x": (dot.x + 0.5) * world.unit,
            "y": (dot.y + 0.5) * world.unit,
            "age": dot.age,
            "genome": dot.genome.genome,
            "color": dot.color,
            "size": dot.size,
            "speed": dot.speed,
            "radius": dot.radius,
            "reproduction_rate": dot.reproduction_rate,
            "lifespan": dot.lifespan,
        }

    if not world.dots or keyboard.is_pressed("s"):
        stop_simulation = True

    print(frame, end="\r")
    frame += 1  # Increment the frame counter

# Save dot_data to a CSV file
simulation_data_df = pd.DataFrame.from_dict(simulation_data, orient="index")
simulation_data_df.to_csv("simulation_data.csv", index_label="frame")
