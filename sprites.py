from settings import pygame


def get_image(name, width, height, scale):
    sheet = pygame.image.load("./enemy/bomber/bomber_engine.png").convert_alpha()
    image = pygame.Surface([width, height]).convert_alpha()
    image.blit(sheet, (0, 0), (0, 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey([0, 0, 0])
    return image
