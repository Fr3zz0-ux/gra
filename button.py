import pygame

class Button():
    def __init__(self, x, y, width, height, name):

        self.rect = pygame.Rect(x, y, width, height)
        self.name = name
        
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def draw_debug(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)