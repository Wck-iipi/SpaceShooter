from settings import pygame, screen, timer, fps
from background import initialize_background, move_background
from sprites import (
    start_animation,
    create_new_sprite_object,
    movement_player_sprite,
    shoot_player_sprite,
)
import shared_state

run = True
background_height, panels, background = initialize_background()

create_new_sprite_object(
    "./player/battlecruiser", 1
)

while run:
    timer.tick(fps)
    screen.fill([255, 255, 255])

    move_background(background_height, background, panels)
    start_animation()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_object = create_new_sprite_object(
                    "./projectiles/torpedo", 2
                )

    movement_player_sprite()
    shoot_player_sprite()

    pygame.display.flip()

pygame.quit()
