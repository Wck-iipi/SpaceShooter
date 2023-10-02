from settings import pygame, screen, timer, fps
from background import initialize_background, move_background
from sprites import get_image

run = True
scroll, background_height, panels, background = initialize_background()
    
frame_0 = get_image("./enemy/bomber", 0, 64, 64, 2)
frame_1 = get_image("./enemy/bomber", 1, 64, 64, 2)
frame_2 = get_image("./enemy/bomber", 2, 64, 64, 2)
frame_3 = get_image("./enemy/bomber", 3, 64, 64, 2)
frame_4 = get_image("./enemy/bomber", 4, 64, 64, 2)
frame_5 = get_image("./enemy/bomber", 5, 64, 64, 2)
frame_6 = get_image("./enemy/bomber", 6, 64, 64, 2)
frame_7 = get_image("./enemy/bomber", 7, 64, 64, 2)
frame_8 = get_image("./enemy/bomber", 8, 64, 64, 2)
frame_9 = get_image("./enemy/bomber", 9, 64, 64, 2)
frame_10 = get_image("./enemy/bomber", 10, 64, 64, 2)

while run:
    timer.tick(fps)
    screen.fill([255, 255, 255])

    scroll = move_background(screen, scroll, background_height, background, panels)
    screen.blit(frame_0, (0, 0))
    screen.blit(frame_1, (500, 500))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()
