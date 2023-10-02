from settings import pygame


def get_image(name, frame_number, width, height, scale):
    sheet_engine = pygame.image.load(name + "engine.png").convert_alpha()
    sheet_base = pygame.image.load(name + "base.png").convert_alpha()
    image = pygame.Surface([width, height], pygame.SRCALPHA).convert_alpha()
    image.blit(sheet_engine, (0, 0), (frame_number * width, 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    return image
