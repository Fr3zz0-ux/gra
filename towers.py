import pygame
import math

class Tower:

    def __init__(self, radius, color, range, x_pos, y_pos):
        self.radius = radius
        self.color = color
        self.range = range + radius
        self.x_pos = x_pos
        self.y_pos = y_pos


    def draw(self, screen):
        pygame.draw.circle(screen, "gray", (self.x_pos, self.y_pos), radius=self.radius + self.range)
        pygame.draw.circle(screen, self.color, (self.x_pos, self.y_pos), radius=self.radius)

    def atack(self, screen, enemy_pos, enemy_x, enemy_y):
        if enemy_pos <= self.range:
            pygame.draw.line(screen, "yellow", (self.x_pos, self.y_pos), (enemy_x, enemy_y))