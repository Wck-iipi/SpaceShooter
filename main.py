from settings import pygame, screen, timer, fps
from background import initialize_background, move_background
from sprites import create_new_sprite_object
from screen_selector import event_selection, return_screen_number, screen_selection
import shared_state

run = True
background_height, panels, background = initialize_background()


while run:
    if shared_state.start_again:
        create_new_sprite_object("./player/battlecruiser", 1)
        shared_state.start_again = False

    timer.tick(fps)
    screen.fill([255, 255, 255])

    move_background(background_height, background, panels)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        run = event_selection(event)

        if return_screen_number() == 1:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet_object = create_new_sprite_object(
                        "./projectiles/torpedo", 2, 0
                    )

    screen_selection()

    pygame.display.flip()

pygame.quit()
