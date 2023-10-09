# TODO: Add a function to add bullets to the ships
# TODO: Every projectile must also have a parent
# and if the projectile must shoot something
# TODO: Generalise projectile_animation function
# further so all the projectiles can now be animated
from settings import pygame, screen
from random import randint
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
    "bolt": {"frames": 5, "width": 9, "height": 9},
}

__animation_cooldown = 150

__is_direction_left = {}

__last_bullet_creation_time = {}

__bullet_motion_direction = {}

__parent_sprite = {}


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
    add_sprite_movement(current_time)

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


def create_new_sprite_object(name, scale=2, parent=None, direction=None):
    index = shared_state.empty_index.popleft()
    shared_state.filled_index.append(index)
    shared_state.animation_list[index] = get_animation_list(name, scale)
    shared_state.sprite_name[index] = name.split("/")[2]

    if name.split("/")[1] == "projectiles":
        __parent_sprite[index] = parent
        if name.split("/")[2] == "torpedo":
            shared_state.x_coordinates[index] = shared_state.x_coordinates[0] + 53
            shared_state.y_coordinates[index] = shared_state.y_coordinates[0]
        elif name.split("/")[2] == "bolt":
            if shared_state.sprite_name[__parent_sprite[index]] == "fighter":
                shared_state.x_coordinates[index] = (
                    shared_state.x_coordinates[__parent_sprite[index]] + 53
                )
                shared_state.y_coordinates[index] = (
                    shared_state.y_coordinates[__parent_sprite[index]] + 90
                )
            elif shared_state.sprite_name[__parent_sprite[index]] == "bomber":
                if direction == "down":
                    shared_state.x_coordinates[index] = (
                        shared_state.x_coordinates[__parent_sprite[index]] + 53
                    )
                    shared_state.y_coordinates[index] = (
                        shared_state.y_coordinates[__parent_sprite[index]] + 90
                    )
                    __bullet_motion_direction[index] = "down"
                elif direction == "up":
                    shared_state.x_coordinates[index] = (
                        shared_state.x_coordinates[__parent_sprite[index]] + 53
                    )
                    shared_state.y_coordinates[index] = (
                        shared_state.y_coordinates[__parent_sprite[index]] 
                    )
                    __bullet_motion_direction[index] = "up"
                elif direction == "left":
                    shared_state.x_coordinates[index] = (
                        shared_state.x_coordinates[__parent_sprite[index]] 
                    )
                    shared_state.y_coordinates[index] = (
                        shared_state.y_coordinates[__parent_sprite[index]] + 45
                    )
                    __bullet_motion_direction[index] = "left"
                elif direction == "right":
                    shared_state.x_coordinates[index] = (
                        shared_state.x_coordinates[__parent_sprite[index]] + 106
                    )
                    shared_state.y_coordinates[index] = (
                        shared_state.y_coordinates[__parent_sprite[index]] + 45
                    )
                    __bullet_motion_direction[index] = "right"

    elif name.split("/")[1] == "enemy":
        shared_state.x_coordinates[index] = randint(0, 900)
        shared_state.y_coordinates[index] = -90


def movement_player_sprite():
    keys = pygame.key.get_pressed()
    if -25 <= shared_state.x_coordinates[0]:
        if keys[pygame.K_LEFT]:
            left_motion(0, 5)

    if shared_state.x_coordinates[0] <= 900:
        if keys[pygame.K_RIGHT]:
            right_motion(0, 5)

    if 0 <= shared_state.y_coordinates[0]:
        if keys[pygame.K_UP]:
            print(shared_state.y_coordinates[0])
            up_motion(0, 5)

    if shared_state.y_coordinates[0] <= 775:
        if keys[pygame.K_DOWN]:
            down_motion(0, 5)


def add_sprite_movement(current_time):
    remove_filled_sprite_index = []
    bolt_to_be_created = []
    for r in shared_state.filled_index:
        if (
            shared_state.sprite_name[r] == "torpedo"
            or shared_state.sprite_name[r] == "bolt"
        ):
            projectile_animation(r)
        elif shared_state.sprite_name[r] == "fighter":
            if r not in __is_direction_left:
                __is_direction_left[r] = randint(0, 1) == 1
            fighter_animation(r)

            time_between_bullets = 400

            if r in __last_bullet_creation_time:
                if (
                    current_time - __last_bullet_creation_time[r]
                    >= time_between_bullets
                ):
                    bolt_to_be_created.append(r)
                    __last_bullet_creation_time[r] = current_time
            else:
                bolt_to_be_created.append(r)
                __last_bullet_creation_time[r] = current_time

        elif shared_state.sprite_name[r] == "scout":
            scout_animation(r)

        elif shared_state.sprite_name[r] == "bomber":
            bomber_animation(r)
            time_between_bullets = 800

            if r in __last_bullet_creation_time:
                if (
                    current_time - __last_bullet_creation_time[r]
                    >= time_between_bullets
                ):
                    bolt_to_be_created.append(r)
                    __last_bullet_creation_time[r] = current_time
            else:
                bolt_to_be_created.append(r)
                __last_bullet_creation_time[r] = current_time

        if delete_sprites_out_of_bounds(r):
            print(shared_state.sprite_name[r] + " is out of bounds")
            remove_filled_sprite_index.append(r)

    for r in bolt_to_be_created:
        if shared_state.sprite_name[r] == "fighter":
            create_new_sprite_object("./projectiles/bolt", 3, r)
        elif shared_state.sprite_name[r] == "bomber":
            create_new_sprite_object("./projectiles/bolt", 3, r, "left")
            create_new_sprite_object("./projectiles/bolt", 3, r, "right")
            create_new_sprite_object("./projectiles/bolt", 3, r, "up")
            create_new_sprite_object("./projectiles/bolt", 3, r, "down")

    for r in remove_filled_sprite_index:
        shared_state.filled_index.remove(r)


def delete_sprites_out_of_bounds(r):
    if (
        shared_state.y_coordinates[r] <= -100
        or shared_state.x_coordinates[r] >= 1100
        or shared_state.y_coordinates[r] >= 1000
    ):
        shared_state.empty_index.appendleft(r)
        shared_state.x_coordinates[r] = 0
        shared_state.y_coordinates[r] = 0
        shared_state.frame_number[r] = 0
        shared_state.animation_list[r] = None
        shared_state.sprite_name[r] = ""
        return True
    else:
        return False


def bomber_animation(r):
    if shared_state.y_coordinates[r] <= 200:
        down_motion(r, 5)


def projectile_animation(r):
    if shared_state.sprite_name[__parent_sprite[r]] == "battlecruiser":
        up_motion(r, 5)

    elif shared_state.sprite_name[__parent_sprite[r]] == "fighter":
        down_motion(r, 10)

    elif shared_state.sprite_name[__parent_sprite[r]] == "bomber":
        if r in __bullet_motion_direction:
            if __bullet_motion_direction[r] == "down":
                down_motion(r, 5)
            elif __bullet_motion_direction[r] == "up":
                up_motion(r, 5)
            elif __bullet_motion_direction[r] == "left":
                left_motion(r, 5)
            elif __bullet_motion_direction[r] == "right":
                right_motion(r, 5)
            elif __bullet_motion_direction[r] == "up_left":
                up_left_motion(r, 5, 5)
            elif __bullet_motion_direction[r] == "up_right":
                up_right_motion(r, 5, 5)
            elif __bullet_motion_direction[r] == "down_left":
                down_left_motion(r, 5, 5)
            elif __bullet_motion_direction[r] == "down_right":
                down_right_motion(r, 5, 5)


def fighter_animation(r):
    if shared_state.x_coordinates[r] >= 900:
        __is_direction_left[r] = True
    if shared_state.x_coordinates[r] <= -70:
        __is_direction_left[r] = False

    if __is_direction_left[r]:
        down_left_motion(r, 3, 1)
    else:
        down_right_motion(r, 3, 1)


def scout_animation(r):
    if shared_state.x_coordinates[r] >= shared_state.x_coordinates[0]:
        down_left_motion(r, 1, 1)
    else:
        down_right_motion(r, 1, 1)


def update_time_projectile(r):
    if __parent_sprite[r] == "fighter":
        pass


def up_motion(r, d):
    shared_state.y_coordinates[r] -= d


def down_motion(r, d):
    shared_state.y_coordinates[r] += d


def right_motion(r, d):
    shared_state.x_coordinates[r] += d


def left_motion(r, d):
    shared_state.x_coordinates[r] -= d


def down_right_motion(r, dx, dy):
    shared_state.y_coordinates[r] += dy
    shared_state.x_coordinates[r] += dx


def down_left_motion(r, dx, dy):
    shared_state.y_coordinates[r] += dy
    shared_state.x_coordinates[r] -= dx


def up_right_motion(r, dx, dy):
    shared_state.y_coordinates[r] -= dy
    shared_state.x_coordinates[r] += dx


def up_left_motion(r, dx, dy):
    shared_state.y_coordinates[r] -= dy
    shared_state.x_coordinates[r] -= dx
