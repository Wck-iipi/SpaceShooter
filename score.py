from settings import screen_width, pygame, screen
import shared_state

def show_score():
    font = pygame.font.SysFont("", 72)

    current_score = shared_state.score
    text_surface = font.render(str(current_score), True, (255, 255, 255))

    text_rect = text_surface.get_rect(right=screen_width, top=0)

    screen.blit(text_surface, text_rect)
