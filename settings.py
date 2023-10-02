import pygame

pygame.init()

timer = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 900

screen = pygame.display.set_mode(
    [screen_width, screen_height], pygame.HWSURFACE | pygame.DOUBLEBUF
)
pygame.display.set_caption("16 bit shooter")
