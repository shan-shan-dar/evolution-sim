import pygame

import graphics as gfx
from world import World
from dot import Dot
import parameters as prm

world = World()

pygame.init()

clock = pygame.time.Clock()

display = pygame.display.set_mode(
    (world.width * world.unit + gfx.SIDE_PANEL, world.height * world.unit)
)

paused = False
fast_forward = False


def draw():

    # Fill the display surface with the background color
    display.fill(world.color)

    if not fast_forward:
        # Draw the grid and dots
        for x in range(world.width):
            for y in range(world.height):
                if isinstance(world.grid[x][y], Dot):
                    dot = world.grid[x][y]
                    gfx.draw_dot(display, world, dot)

    # Draw the UI surface
    ui_surface = gfx.draw_ui(world)
    display.blit(ui_surface, (world.width * world.unit, 0))

    # Draw pause indicator
    if paused:
        gfx.draw_pause(display)

    # Draw "END" message if population is extinct
    if not world.dots:
        gfx.draw_end_message(display, world)

    # Draw static message if in fast forward mode
    if fast_forward:
        font = pygame.font.Font(None, 36)
        text = font.render("Fast Forward Mode", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(world.width * world.unit // 2, world.height * world.unit // 2)
        )
        display.blit(text, text_rect)

    pygame.display.update()


world.spawn(prm.STARTING_POPULATION)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            if event.key == pygame.K_f:
                fast_forward = not fast_forward

    if not paused:
        if fast_forward:
            world.update()
            clock.tick(prm.FAST_FORWARD_RATE * prm.FPS)
        else:
            world.update()
            clock.tick(prm.FPS)

    draw()
