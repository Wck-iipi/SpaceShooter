import math
from settings import pygame, screen_width, screen_height


def initialize_background(background_name="Blue_Nebula.png"):
    background = pygame.image.load("./backgrounds/" + background_name).convert()
    background_height = background.get_height()
    background = pygame.transform.scale(background, (screen_width, background_height))

    scroll = 0
    panels = math.ceil(screen_height / background_height) + 2

    return scroll, background_height, panels, background


def move_background(screen, scroll, background_height, background, panels):
    for i in range(panels):
        screen.blit(background, (0, (i - 1) * background_height + scroll))

    scroll += 3
    if abs(scroll)-background_height>= 0:
        scroll = 0
    return scroll
