from settings import pygame, screen, timer, fps
from background import initialize_background, move_background
from sprites import get_animation_list, start_animation

run = True
background_height, panels, background = initialize_background()

bomber_animation = get_animation_list("./enemy/bomber", 5)

while run:
    timer.tick(fps)
    screen.fill([255, 255, 255])

    move_background(background_height, background, panels)
    start_animation(bomber_animation, 0, 0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()
