from settings import pygame
#No of frames in the sprite sheet of engine
#Bomber - 10
#Dreadnought - 11
#Fighter - 10
#Frigate - 12
#Scout - 10
#Support_ship - 10
#Player - 8


def get_image(name, frame_number, width, height, scale):
    base = pygame.image.load(name + "/base.png").convert_alpha()
    sheet_engine = pygame.image.load(name + "/engine.png").convert_alpha()

    image = pygame.Surface([width, height], pygame.SRCALPHA).convert_alpha()
    image.blit(sheet_engine, (0, 0), (frame_number * width, 0, width, height))
    image.blit(base, (0, 0))
    image = pygame.transform.scale(image, (width * scale, height * scale))

    return image
