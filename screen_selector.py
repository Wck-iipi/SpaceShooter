from collections import deque
from settings import pygame, screen_width, screen_height, screen
from sprites import start_animation, movement_player_sprite, collision_detect
from score import show_score
from enemy_sequence import enemy_sequence_start
import shared_state

BACKGROUND_COLOR = (0, 0, 0)
GAME_TITLE = "Stellar Skies"
START_BUTTON_IMAGE = pygame.image.load("./backgrounds/start.png")

pygame.display.set_caption(GAME_TITLE)

button_width, button_height = START_BUTTON_IMAGE.get_size()
button_width //= 2
button_height //= 2

button_x = (screen_width - button_width) // 2
button_y = (screen_height - button_height) // 2

font = pygame.font.Font(None, 96)

title_text = font.render(GAME_TITLE, True, (232, 84, 195))
title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 3))

button_font = pygame.font.Font(None, 48)

retry_button_text = button_font.render("Retry", True, (255, 255, 255))
end_button_text = button_font.render("End", True, (255, 255, 255))

retry_button_x = (screen_width - retry_button_text.get_width()) // 2
retry_button_y = screen_height // 2
end_button_x = (screen_width - end_button_text.get_width()) // 2
end_button_y = retry_button_y + retry_button_text.get_height() + 20

game_over_font = pygame.font.Font(None, 72)

game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 4))


def event_selection(event):
    if shared_state.screen_number == 0:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (
                button_x < mouse_x < button_x + button_width
                and button_y < mouse_y < button_y + button_height
            ):
                shared_state.screen_number = 1
    elif shared_state.screen_number == 2:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (
                retry_button_x
                < mouse_x
                < retry_button_x + retry_button_text.get_width()
                and retry_button_y
                < mouse_y
                < retry_button_y + retry_button_text.get_height()
            ):
                shared_state.screen_number = 0
            elif (
                end_button_x < mouse_x < end_button_x + end_button_text.get_width()
                and end_button_y < mouse_y < end_button_y + end_button_text.get_height()
            ):
                return False
    return True


def screen_selection():
    if shared_state.screen_number == 0:
        screen.blit(title_text, title_rect)
        screen.blit(
            pygame.transform.scale(START_BUTTON_IMAGE, (button_width, button_height)),
            (button_x, button_y),
        )
    elif shared_state.screen_number == 2:
        screen.blit(game_over_text, game_over_rect)
        screen.blit(retry_button_text, (retry_button_x, retry_button_y))
        screen.blit(end_button_text, (end_button_x, end_button_y))
        initialize_values()
    elif shared_state.screen_number == 1:
        main_game_procedure()


def return_screen_number():
    return shared_state.screen_number


def main_game_procedure():
    enemy_sequence_start()
    start_animation()
    movement_player_sprite()
    collision_detect()
    show_score()


def initialize_values():
    shared_state.frame_number = [0 for _ in range(500)]
    shared_state.sprite_name = ["" for _ in range(500)]
    shared_state.scroll = 0
    shared_state.last_update = 0
    shared_state.animation_list = [None for _ in range(500)]
    shared_state.rotation = [0 for _ in range(500)]
    shared_state.x_coordinates = [0 for _ in range(500)]
    shared_state.x_coordinates[0] = 400
    shared_state.y_coordinates = [0 for _ in range(500)]
    shared_state.y_coordinates[0] = 780
    shared_state.empty_index = deque(r for r in range(500))
    shared_state.filled_index = deque()
    shared_state.score = 0
    shared_state.start_again = True
    shared_state.first_update = True
