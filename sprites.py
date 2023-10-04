from settings import pygame, screen
import shared_state

# No of frames in the sprite sheet of engine
# Bomber - 10
# Dreadnought - 11
# Fighter - 10
# Frigate - 12
# Scout - 10
# Support_ship - 10
# Battlecruiser - 8

__ship_information = {
    "bomber": {"frames": 10, "width": 64, "height": 64},
    "dreadnought": {"frames": 11, "width": 128, "height": 128},
    "fighter": {"frames": 10, "width": 64, "height": 64},
    "frigate": {"frames": 12, "width": 64, "height": 64},
    "scout": {"frames": 10, "width": 64, "height": 64},
    "support_ship": {"frames": 10, "width": 64, "height": 64},
    "battlecruiser": {"frames": 8, "width": 128, "height": 128},
}

__animation_cooldown = 150


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


def get_animation_list(name, scale=2):
    ship_name = name.split("/")[2]
    animation_list = []

    for i in range(__ship_information[ship_name]["frames"]):
        animation_list.append(get_image(name, i, scale))

    return animation_list


def start_animation(animation_list, x, y):
    current_time = pygame.time.get_ticks()

    if current_time - shared_state.last_update >= __animation_cooldown:
        shared_state.frame_number += 1
        shared_state.last_update = current_time
        if shared_state.frame_number >= len(animation_list):
            shared_state.frame_number = 0

    screen.blit(animation_list[shared_state.frame_number], (x, y))


def create_new_sprite_object(name, scale=2):
    index = shared_state.empty_index.popleft()
    shared_state.filled_index.appendleft(index)

    shared_state.animation_list[index] = get_animation_list(name, scale)
    # Represents the animation object and the shared_state coordinate index
    sprite_object = [
        index,
        shared_state.animation_list[index]
    ]
    return sprite_object

def movement_player_sprite():
    keys = pygame.key.get_pressed()
    if -25 <= shared_state.x_coordinates[0]:
        if keys[pygame.K_LEFT]:
            shared_state.x_coordinates[0] -= 5

    if shared_state.x_coordinates[0] <= 900:
        if keys[pygame.K_RIGHT]:
            shared_state.x_coordinates[0] += 5

    if 0 <= shared_state.y_coordinates[0]:
        if keys[pygame.K_UP]:
            shared_state.y_coordinates[0] -= 5

    if shared_state.y_coordinates[0] <= 775:
        if keys[pygame.K_DOWN]:
            shared_state.y_coordinates[0] += 5
    print(shared_state.x_coordinates[0], shared_state.y_coordinates[0])

