import pygame


def draw_dot(display, world, dot):
    center_x = (dot.x + 0.5) * world.unit
    center_y = (dot.y + 0.5) * world.unit

    radius = dot.size * world.unit

    pygame.draw.circle(display, dot.color, (center_x, center_y), radius)


def draw_pause(display):
    pause_surf = pygame.Surface((40, 40), pygame.SRCALPHA)
    pause_surf.fill((0, 0, 0, 179))
    pygame.draw.rect(pause_surf, (255, 255, 255, 179), pygame.Rect(10, 10, 10, 20))
    pygame.draw.rect(pause_surf, (255, 255, 255, 179), pygame.Rect(25, 10, 10, 20))
    display.blit(pause_surf, (10, 10))


def draw_end_message(display, world):
    font = pygame.font.SysFont(None, 48)
    text = font.render("EXTINCT", True, (255, 255, 255))
    text_rect = text.get_rect(
        center=(world.width * world.unit // 2, world.height * world.unit // 2)
    )
    display.blit(text, text_rect)


SIDE_PANEL = 400


def draw_ui(world):
    # Create a new surface to display the extra UI
    ui_surface = pygame.Surface((SIDE_PANEL, world.height * world.unit))
    ui_surface.fill((243, 243, 243, 255))

    # Add the age of the simulation to the UI surface
    font = pygame.font.Font(None, 24)

    elapsed_text = font.render(
        "Time elapsed: " + str(world.time_elapsed), True, (0, 0, 0)
    )

    # Add the average generation count to the UI surface

    lifespan_text = font.render(
        "Approx. generations: " + str(world.approx_generations),
        True,
        (0, 0, 0),
    )

    population_text = font.render(
        "Population: " + str(len(world.dots)), True, (0, 0, 0)
    )

    ui_surface.blit(elapsed_text, (10, 10))

    ui_surface.blit(lifespan_text, (10, 40))

    ui_surface.blit(population_text, (10, 70))

    return ui_surface
