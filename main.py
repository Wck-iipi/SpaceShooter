from settings import pygame, screen, timer, fps
from background import initialize_background, move_background
from sprites import get_image

run = True
scroll, background_height, panels, background = initialize_background()
    
frame_0 = get_image("./enemy/bomber/bomber", 3, 64, 64, 5)
frame_1 = get_image("./enemy/bomber/bomber", 0, 64, 64, 5)

while run:
    timer.tick(fps)
    screen.fill([255, 255, 255])

    scroll = move_background(screen, scroll, background_height, background, panels)
    screen.blit(frame_0, (0, 0))
    screen.blit(frame_1, (100, 100))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()
