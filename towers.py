

import pygame
import math

class Tower:

    def __init__(self, asset_path, scale_x, scale_y, towerRange, damage, cooldown, x_pos, y_pos):

        # Przygotowanie lufy
        self.original_top = pygame.image.load(asset_path)
        self.top_image = pygame.transform.scale(self.original_top, (scale_x, scale_y))
        self.top_rect = self.top_image.get_rect(midbottom = (x_pos, y_pos + 20))

        # Przygotowanie obrazka
        self.original_base = pygame.image.load("Assets/Tower.png")
        self.base_image = pygame.transform.scale(self.original_base, (50, 50))
        self.base_rect = self.base_image.get_rect(center = (x_pos, y_pos))

        # Statystki
        self.range = towerRange
        self.damage = damage
        self.last_attack_time = 0
        self.cooldown = cooldown
        self.x_pos = x_pos
        self.y_pos = y_pos


    def draw(self, screen):
        ### Pomocnicze do rysowania zasiegu wiezy ###
        #pygame.draw.circle(screen, "gray", (self.x_pos, self.y_pos), radius=self.radius + self.range)

        screen.blit(self.base_image, self.base_rect)
        screen.blit(self.top_image, self.top_rect)



    def attack(self, screen, enemy, distance):

        current_time = pygame.time.get_ticks()

        if distance <= self.range:
            ### Pomocnicze do rysowania wzroku wiezy
            #pygame.draw.line(screen, "yellow", (self.x_pos, self.y_pos), (enemy.x, enemy.y))

            if current_time - self.last_attack_time >= self.cooldown:
                enemy.take_damage(self.damage)

                self.last_attack_time = current_time


class Cannon(Tower):
    def __init__(self, x_pos, y_pos):
        super().__init__(asset_path = "Assets/Cannon.png", scale_x= 35, scale_y = 65 ,towerRange = 100, damage = 30, cooldown = 400, x_pos = x_pos, y_pos = y_pos)