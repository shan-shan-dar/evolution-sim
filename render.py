import pygame
import pandas as pd
import ast

import graphics as gfx
from world import World
from dot import Dot
import parameters as prm

pygame.init()

clock = pygame.time.Clock()

display = pygame.display.set_mode(
    (prm.WORLD_WIDTH * prm.UNIT, prm.WORLD_HEIGHT * prm.UNIT + prm.INDICATOR_HEIGHT)
)

paused = False
speed = prm.DEFAULT_SPEED
speed_indicator_pos = 0

simulation_data_df = pd.read_csv("simulation_data.csv", index_col=0)

frame_count = -1
indicator_pos = 0

move_left = False
move_right = False

frame_delay = 0  # Delay between frame updates
frame_delay_counter = 0  # Counter to keep track of delay


def draw(frame_count):
    if frame_count >= simulation_data_df.index.max():
        # End of data, display end screen
        gfx.draw_stop(display)
    else:
        display.fill(prm.WORLD_COLOR)
        for dot in simulation_data_df.loc[frame_count]:
            if not pd.isna(dot):
                dot = ast.literal_eval(dot)
                gfx.draw_dot(display, dot)

        # Draw pause indicator
        if paused:
            gfx.draw_pause(display)

        # Update indicator position
        indicator_pos = int(
            (frame_count + 1)
            / simulation_data_df.index.max()
            * (prm.WORLD_WIDTH * prm.UNIT)
        )

        # Draw indicator
        gfx.draw_indicator(display, indicator_pos)

    pygame.display.update()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_UP:
                speed += prm.SPEED_INCREMENT
            elif event.key == pygame.K_DOWN:
                speed -= prm.SPEED_INCREMENT
            elif event.key == pygame.K_RIGHT:
                move_right = True
            elif event.key == pygame.K_LEFT:
                move_left = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                move_right = False
            elif event.key == pygame.K_LEFT:
                move_left = False

    if move_right:
        frame_delay_counter += 1
        if frame_delay_counter >= frame_delay:
            frame_delay_counter = 0
            frame_count += 1
            frame_count = min(frame_count, simulation_data_df.index.max())

    if move_left:
        frame_delay_counter += 1
        if frame_delay_counter >= frame_delay:
            frame_delay_counter = 0
            frame_count -= 1
            frame_count = max(frame_count, 0)

    if not paused:
        clock.tick(speed)
        frame_delay = int(speed / prm.DEFAULT_SPEED)  # Set delay based on speed
        frame_count += 1

    draw(frame_count)
