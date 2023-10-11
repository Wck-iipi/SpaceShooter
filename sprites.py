from typing import Dict
from settings import pygame, screen
from random import randint
import shared_state

__sprite_information = {
    "bomber": {"frames": 10, "width": 64, "height": 64, "destruction_frames": 8},
    "dreadnought": {
        "frames": 11,
        "width": 128,
        "height": 128,
        "destruction_frames": 12,
    },
    "fighter": {"frames": 10, "width": 64, "height": 64, "destruction_frames": 9},
    "frigate": {"frames": 12, "width": 64, "height": 64, "destruction_frames": 9},
    "scout": {"frames": 10, "width": 64, "height": 64, "destruction_frames": 10},
    "support_ship": {"frames": 10, "width": 64, "height": 64, "destruction_frames": 10},
    "battlecruiser": {
        "frames": 8,
        "width": 128,
        "height": 128,
        "destruction_frames": 18,
    },
    "torpedo": {"frames": 3, "width": 11, "height": 32},
    "bolt": {"frames": 5, "width": 9, "height": 9},
}

__animation_cooldown = 150

__is_direction_left = {}

__last_bullet_creation_time: Dict[int, int] = {}

__bullet_motion_direction = {}

__parent_sprite = {}

__parent_sprite_name = {}

__delete_after_destruction = {}


def get_image(name, frame_number, scale, destroy):
    if not destroy:
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
    else:
        sheet = pygame.image.load(name + "/destruction.png").convert_alpha()

        ship_name = name.split("/")[2]
        width = __sprite_information[ship_name]["width"]
        height = __sprite_information[ship_name]["height"]

        image = pygame.Surface([width, height], pygame.SRCALPHA).convert_alpha()
        image.blit(sheet, (0, 0), (frame_number * width, 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))

        return image


def get_animation_list(name, destroy, scale=2):
    ship_name = name.split("/")[2]
    animation_list = []

    if not destroy:
        for i in range(__sprite_information[ship_name]["frames"]):
            animation_list.append(get_image(name, i, scale, destroy))
    else:
        for i in range(__sprite_information[ship_name]["destruction_frames"]):
            animation_list.append(get_image(name, i, scale, destroy))

    return animation_list


def start_animation():
    current_time = pygame.time.get_ticks()
    time_diff_bool = current_time - shared_state.last_update >= __animation_cooldown
    add_sprite_movement(current_time)
    delete_objects = []

    for r in shared_state.filled_index:
        x = shared_state.x_coordinates[r]
        y = shared_state.y_coordinates[r]
        if time_diff_bool:
            shared_state.frame_number[r] += 1
            shared_state.last_update = current_time
            if shared_state.frame_number[r] == len(shared_state.animation_list[r]) - 1:
                if r in __delete_after_destruction:
                    if shared_state.sprite_name[r] == "bomber":
                        shared_state.score += 1000
                    elif shared_state.sprite_name[r] == "scout":
                        shared_state.score += 100
                    elif shared_state.sprite_name[r] == "fighter":
                        shared_state.score += 300
                    elif shared_state.sprite_name[r] == "support_ship":
                        shared_state.score += 500
                    delete_objects.append(r)
            elif shared_state.frame_number[r] >= len(shared_state.animation_list[r]):
                shared_state.frame_number[r] = 0
        image = shared_state.animation_list[r][shared_state.frame_number[r]]
        screen.blit(pygame.transform.rotate(image, shared_state.rotation[r]), (x, y))
    for r in delete_objects:
        shared_state.empty_index.append(r)
        shared_state.filled_index.remove(r)
        shared_state.sprite_name[r] = ""
        shared_state.animation_list[r] = []
        shared_state.x_coordinates[r] = 0
        shared_state.y_coordinates[r] = 0
        shared_state.rotation[r] = 0
        shared_state.frame_number[r] = 0


def create_new_sprite_object(name, scale=2, parent=-1, direction="", destroy=False):
    index = shared_state.empty_index.popleft()

    if destroy:
        __delete_after_destruction[index] = True

    shared_state.filled_index.append(index)
    shared_state.animation_list[index] = get_animation_list(name, destroy, scale)
    shared_state.sprite_name[index] = name.split("/")[2]
    shared_state.rotation[index] = 0

    if name.split("/")[1] == "projectiles":
        __parent_sprite[index] = parent
        __parent_sprite_name[index] = shared_state.sprite_name[parent]
        if name.split("/")[2] == "torpedo":
            shared_state.x_coordinates[index] = shared_state.x_coordinates[0] + 53
            shared_state.y_coordinates[index] = shared_state.y_coordinates[0]
        elif name.split("/")[2] == "bolt":
            if __parent_sprite_name[index] == "fighter":
                shared_state.rotation[index] = 180
                shared_state.x_coordinates[index] = (
                    shared_state.x_coordinates[__parent_sprite[index]] + 53
                )
                shared_state.y_coordinates[index] = (
                    shared_state.y_coordinates[__parent_sprite[index]] + 90
                )
            elif __parent_sprite_name[index] == "bomber":
                shared_state.rotation[index] = 180
                if direction == "down":
                    shared_state.x_coordinates[index] = (
                        shared_state.x_coordinates[__parent_sprite[index]] + 53
                    )
                    shared_state.y_coordinates[index] = (
                        shared_state.y_coordinates[__parent_sprite[index]] + 90
                    )
                    shared_state.rotation[index] = 180
                    __bullet_motion_direction[index] = "down"
                elif direction == "up":
                    shared_state.x_coordinates[index] = (
                        shared_state.x_coordinates[__parent_sprite[index]] + 53
                    )
                    shared_state.y_coordinates[index] = shared_state.y_coordinates[
                        __parent_sprite[index]
                    ]
                    shared_state.rotation[index] = 0
                    __bullet_motion_direction[index] = "up"
                elif direction == "left":
                    shared_state.x_coordinates[index] = shared_state.x_coordinates[
                        __parent_sprite[index]
                    ]
                    shared_state.y_coordinates[index] = (
                        shared_state.y_coordinates[__parent_sprite[index]] + 45
                    )
                    shared_state.rotation[index] = 90
                    __bullet_motion_direction[index] = "left"
                elif direction == "right":
                    shared_state.x_coordinates[index] = (
                        shared_state.x_coordinates[__parent_sprite[index]] + 106
                    )
                    shared_state.y_coordinates[index] = (
                        shared_state.y_coordinates[__parent_sprite[index]] + 45
                    )
                    shared_state.rotation[index] = -90
                    __bullet_motion_direction[index] = "right"

            elif __parent_sprite_name[index] == "support_ship":
                shared_state.rotation[index] = -90
                shared_state.x_coordinates[index] = (
                    shared_state.x_coordinates[__parent_sprite[index]] + 106
                )
                shared_state.y_coordinates[index] = (
                    shared_state.y_coordinates[__parent_sprite[index]] + 45
                )

    elif name.split("/")[1] == "enemy":
        if index not in __delete_after_destruction:
            if shared_state.sprite_name[index] != "support_ship":
                shared_state.rotation[index] = 180
                shared_state.x_coordinates[index] = randint(0, 900)
                shared_state.y_coordinates[index] = -90
            else:
                shared_state.rotation[index] = -90
                shared_state.x_coordinates[index] = -30
                shared_state.y_coordinates[index] = -90
        else:
            shared_state.rotation[index] = shared_state.rotation[parent]
            shared_state.x_coordinates[index] = shared_state.x_coordinates[parent]
            shared_state.y_coordinates[index] = shared_state.y_coordinates[parent]


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

        elif shared_state.sprite_name[r] == "support_ship":
            support_ship_animation(r)
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

        if delete_sprites_out_of_bounds(r, current_time):
            print(shared_state.sprite_name[r] + " is out of bounds")
            remove_filled_sprite_index.append(r)

    for r in bolt_to_be_created:
        if shared_state.sprite_name[r] == "bomber":
            create_new_sprite_object("./projectiles/bolt", 3, r, "left")
            create_new_sprite_object("./projectiles/bolt", 3, r, "right")
            create_new_sprite_object("./projectiles/bolt", 3, r, "up")
            create_new_sprite_object("./projectiles/bolt", 3, r, "down")
        else:
            create_new_sprite_object("./projectiles/bolt", 3, r)

    for r in remove_filled_sprite_index:
        shared_state.filled_index.remove(r)


def delete_sprites_out_of_bounds(r, current_time=None):
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
    if r not in __delete_after_destruction:
        if shared_state.y_coordinates[r] <= 200:
            down_motion(r, 5)


def projectile_animation(r):
    if __parent_sprite_name[r] == "battlecruiser":
        up_motion(r, 5)

    elif __parent_sprite_name[r] == "fighter":
        down_motion(r, 5)

    elif __parent_sprite_name[r] == "bomber":
        if r in __bullet_motion_direction:
            if __bullet_motion_direction[r] == "down":
                down_motion(r, 5)
            elif __bullet_motion_direction[r] == "up":
                up_motion(r, 5)
            elif __bullet_motion_direction[r] == "left":
                left_motion(r, 5)
            elif __bullet_motion_direction[r] == "right":
                right_motion(r, 5)
    elif __parent_sprite_name[r] == "support_ship":
        right_motion(r, 5)


def fighter_animation(r):
    if r not in __delete_after_destruction:
        if shared_state.x_coordinates[r] >= 900:
            __is_direction_left[r] = True
        if shared_state.x_coordinates[r] <= -70:
            __is_direction_left[r] = False

        if __is_direction_left[r]:
            down_left_motion(r, 3, 1)
        else:
            down_right_motion(r, 3, 1)


def collision_detect():
    torpedo_list = []
    bolt_list = []
    remove_states = []
    destruction_objects = []

    for r in shared_state.filled_index:
        if shared_state.sprite_name[r] == "torpedo":
            torpedo_list.append(r)
        elif shared_state.sprite_name[r] == "bolt":
            bolt_list.append(r)

    player_rect = pygame.Rect(
        shared_state.x_coordinates[0],
        shared_state.y_coordinates[0],
        __sprite_information[shared_state.sprite_name[0]]["width"],
        __sprite_information[shared_state.sprite_name[0]]["height"],
    )

    for r in shared_state.filled_index:
        obj_rect = pygame.Rect(
            shared_state.x_coordinates[r],
            shared_state.y_coordinates[r],
            __sprite_information[shared_state.sprite_name[r]]["width"],
            __sprite_information[shared_state.sprite_name[r]]["height"],
        )
        if (
            r != 0
            and shared_state.sprite_name[r] != "torpedo"
            and r not in __delete_after_destruction
            and shared_state.sprite_name[r] != "bolt"
        ):
            for torpedo in torpedo_list:
                torpedo_rect = pygame.Rect(
                    shared_state.x_coordinates[torpedo],
                    shared_state.y_coordinates[torpedo],
                    __sprite_information[shared_state.sprite_name[torpedo]]["width"],
                    __sprite_information[shared_state.sprite_name[torpedo]]["height"],
                )
                if obj_rect.colliderect(torpedo_rect):
                    destruction_objects.append(r)
                    remove_states.append(r)
                    remove_states.append(torpedo)
                    break
        elif r != 0 and shared_state.sprite_name[r] != "torpedo":
            if obj_rect.colliderect(player_rect):
                shared_state.screen_number = 2

    for r in destruction_objects:
        create_new_sprite_object(
            "./enemy/" + shared_state.sprite_name[r], 2, r, "", True
        )
        print(shared_state.sprite_name[r] + " is destroyed")

    for r in remove_states:
        shared_state.filled_index.remove(r)
        shared_state.empty_index.appendleft(r)
        shared_state.x_coordinates[r] = 0
        shared_state.y_coordinates[r] = 0
        shared_state.frame_number[r] = 0
        shared_state.animation_list[r] = None
        shared_state.sprite_name[r] = ""
    pass


def support_ship_animation(r):
    if r not in __delete_after_destruction:
        down_motion(r, 3)


def scout_animation(r):
    if r not in __delete_after_destruction:
        if shared_state.x_coordinates[r] >= shared_state.x_coordinates[0]:
            down_left_motion(r, 1, 1)
        else:
            down_right_motion(r, 1, 1)


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
