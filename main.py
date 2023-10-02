from settings import pygame, screen, timer, fps
from background import initialize_background, move_background

run = True
scroll, background_height, panels, background = initialize_background()
sprite_sheet_image = pygame.image.load("./enemy/bomber/engine.png").convert_alpha()

while run:
    timer.tick(fps)
    screen.fill([255, 255, 255])

    scroll = move_background(screen, scroll, background_height, background, panels)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()
