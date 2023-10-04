from settings import pygame, screen, timer, fps
from background import initialize_background, move_background
from sprites import (
    get_animation_list,
    start_animation,
    create_new_sprite_object,
    movement_player_sprite,
)
import shared_state

run = True
background_height, panels, background = initialize_background()

bomber_object = create_new_sprite_object(
    "./player/battlecruiser", 1
)

while run:
    timer.tick(fps)
    screen.fill([255, 255, 255])

    move_background(background_height, background, panels)

    for r in shared_state.filled_index:
        start_animation(
            shared_state.animation_list[r],
            shared_state.x_coordinates[r],
            shared_state.y_coordinates[r],
        )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    movement_player_sprite()

    pygame.display.flip()

pygame.quit()
