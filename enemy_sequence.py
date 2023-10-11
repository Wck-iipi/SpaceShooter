import random
from settings import pygame
from sprites import create_new_sprite_object, pygame, shared_state
import shared_state


def enemy_sequence_start():
    current_time = pygame.time.get_ticks()
    time_diff_bool = current_time - shared_state.last_update_create >= 7000

    if time_diff_bool or shared_state.first_update:
        scout = random.randint(0, 2)
        fighter = random.randint(0, 2)
        support = random.randint(0, 1)
        bomb = random.randint(0, 1)
        scout_fighter_support_bomber = [scout, fighter, support, bomb]

        for _ in range(scout_fighter_support_bomber[0]):
            create_new_sprite_object("./enemy/scout", 2)
        for _ in range(scout_fighter_support_bomber[1]):
            create_new_sprite_object("./enemy/fighter", 2)
        for _ in range(scout_fighter_support_bomber[2]):
            create_new_sprite_object("./enemy/support_ship", 2)
        for _ in range(scout_fighter_support_bomber[3]):
            create_new_sprite_object("./enemy/bomber", 2)
        shared_state.first_update = False
        shared_state.last_update_create = current_time
