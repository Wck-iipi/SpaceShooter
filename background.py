import math
import shared_state
from settings import pygame, screen_width, screen_height, screen


def initialize_background(background_name="Blue_Nebula.png"):
    background = pygame.image.load("./backgrounds/" + background_name).convert()
    background_height = background.get_height()
    background = pygame.transform.scale(background, (screen_width, background_height))

    shared_state.scroll = 0
    panels = math.ceil(screen_height / background_height) + 2

    return background_height, panels, background


def move_background(background_height, background, panels):
    scroll = shared_state.scroll
    for i in range(panels):
        screen.blit(background, (0, (i - 1) * background_height + scroll))

    shared_state.scroll += 3
    if abs(scroll)-background_height>= 0:
        shared_state.scroll = 0
