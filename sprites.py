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

__sprite_information = {
    "bomber": {"frames": 10, "width": 64, "height": 64},
    "dreadnought": {"frames": 11, "width": 128, "height": 128},
    "fighter": {"frames": 10, "width": 64, "height": 64},
    "frigate": {"frames": 12, "width": 64, "height": 64},
    "scout": {"frames": 10, "width": 64, "height": 64},
    "support_ship": {"frames": 10, "width": 64, "height": 64},
    "battlecruiser": {"frames": 8, "width": 128, "height": 128},
    "torpedo": {"frames": 3, "width": 11, "height": 32},
}

__animation_cooldown = 150


def get_image(name, frame_number, scale):
    if name.split("/")[1] == "enemy" or name.split("/")[1] == "player":
        base = pygame.image.load(name + "/base.png").convert_alpha()
        sheet_engine = pygame.image.load(name + "/engine.png").convert_alpha()

        ship_name = name.split("/")[2]
        width = __sprite_information[ship_name]["width"]
        height = __sprite_information[ship_name]["height"]

        image = pygame.Surface([width, height], pygame.SRCALPHA).convert_alpha()
        image.blit(sheet_engine, (0, 0), (frame_number * width, 0, width, height))
        image.blit(base, (0, 0))
        image = pygame.transform.scale(image, (width * scale, height * scale))

        return image

    elif name.split("/")[1] == "projectiles":
        sheet = pygame.image.load(name + "/main.png").convert_alpha()
        projectile_name = name.split("/")[2]
        width = __sprite_information[projectile_name]["width"]
        height = __sprite_information[projectile_name]["height"]

        image = pygame.Surface([width, height], pygame.SRCALPHA).convert_alpha()
        image.blit(sheet, (0, 0), (frame_number * width, 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))

        return image


def get_animation_list(name, scale=2):
    ship_name = name.split("/")[2]
    animation_list = []

    for i in range(__sprite_information[ship_name]["frames"]):
        animation_list.append(get_image(name, i, scale))

    return animation_list


def start_animation():
    current_time = pygame.time.get_ticks()
    time_diff_bool = current_time - shared_state.last_update >= __animation_cooldown
    add_sprite_movement()

    for r in shared_state.filled_index:
        x = shared_state.x_coordinates[r]
        y = shared_state.y_coordinates[r]
        if time_diff_bool:
            shared_state.frame_number[r] += 1
            shared_state.last_update = current_time
            if shared_state.frame_number[r] >= len(shared_state.animation_list[r]):
                shared_state.frame_number[r] = 0
        screen.blit(
            shared_state.animation_list[r][shared_state.frame_number[r]], (x, y)
        )


def create_new_sprite_object(name, scale=2):
    index = shared_state.empty_index.popleft()
    shared_state.filled_index.append(index)
    shared_state.animation_list[index] = get_animation_list(name, scale)
    shared_state.sprite_name[index] = name.split("/")[2]

    if name.split("/")[1] == "projectiles":
        if name.split("/")[2] == "torpedo":
            shared_state.x_coordinates[index] = shared_state.x_coordinates[0] + 53
            shared_state.y_coordinates[index] = shared_state.y_coordinates[0]


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


def add_sprite_movement():
    remove_filled_sprite_index = []
    for r in shared_state.filled_index:
        if shared_state.sprite_name[r] == "torpedo":
            if torpedo_animation(r):
                remove_filled_sprite_index.append(r)

        if (
            shared_state.y_coordinates[r] <= -100
            or shared_state.x_coordinates[r] >= 1100
        ):
            shared_state.empty_index.appendleft(r)
            shared_state.x_coordinates[r] = 0
            shared_state.y_coordinates[r] = 0
            shared_state.frame_number[r] = 0
            shared_state.animation_list[r] = None
            shared_state.sprite_name[r] = ""
            remove_filled_sprite_index.append(r)

    for r in remove_filled_sprite_index:
        shared_state.filled_index.remove(r)


def torpedo_animation(r):
    shared_state.y_coordinates[r] -= 5
