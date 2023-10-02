from settings import pygame

# No of frames in the sprite sheet of engine
# Bomber - 10
# Dreadnought - 11
# Fighter - 10
# Frigate - 12
# Scout - 10
# Support_ship - 10
# Player - 8

__ship_information = {
    "bomber": {"frames": 10, "width": 64, "height": 64},
    "dreadnought": {"frames": 11, "width": 128, "height": 128},
    "fighter": {"frames": 10, "width": 64, "height": 64},
    "frigate": {"frames": 12, "width": 64, "height": 64},
    "scout": {"frames": 10, "width": 64, "height": 64},
    "support_ship": {"frames": 10, "width": 64, "height": 64},
    "player": {"frames": 8, "width": 128, "height": 128},
}


def get_image(name, frame_number, scale):
    base = pygame.image.load(name + "/base.png").convert_alpha()
    sheet_engine = pygame.image.load(name + "/engine.png").convert_alpha()

    ship_name = name.split("/")[2]
    width = __ship_information[ship_name]["width"]
    height = __ship_information[ship_name]["height"]

    image = pygame.Surface([width, height], pygame.SRCALPHA).convert_alpha()
    image.blit(sheet_engine, (0, 0), (frame_number * width, 0, width, height))
    image.blit(base, (0, 0))
    image = pygame.transform.scale(image, (width * scale, height * scale))

    return image
