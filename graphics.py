import pygame
import parameters as prm


def draw_dot(display, dot):
    center_x = (dot["x"] + 0.5) * prm.UNIT
    center_y = (dot["y"] + 0.5) * prm.UNIT

    radius = dot["size"] * prm.UNIT

    pygame.draw.circle(display, dot["color"], (center_x, center_y), radius)


def draw_pause(display):
    pause_surf = pygame.Surface((40, 40), pygame.SRCALPHA)
    pause_surf.fill((0, 0, 0, 179))
    pygame.draw.rect(pause_surf, (255, 255, 255, 179), pygame.Rect(10, 10, 10, 20))
    pygame.draw.rect(pause_surf, (255, 255, 255, 179), pygame.Rect(25, 10, 10, 20))
    display.blit(pause_surf, (10, 10))


def draw_stop(display):
    stop_surf = pygame.Surface((40, 40), pygame.SRCALPHA)
    stop_surf.fill((0, 0, 0, 179))
    pygame.draw.rect(stop_surf, (255, 255, 255, 179), pygame.Rect(10, 10, 20, 20))
    display.blit(stop_surf, (10, 10))


def draw_indicator(display, position):
    indicator_height = prm.INDICATOR_HEIGHT
    indicator_color = prm.INDICATOR_COLOR
    pygame.draw.rect(
        display,
        indicator_color,
        pygame.Rect(0, prm.WORLD_HEIGHT * prm.UNIT, position, indicator_height),
    )
