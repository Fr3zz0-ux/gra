import pygame
import math

class Tower:

    def __init__(self, radius, color, towerRange, damage, cooldown, x_pos, y_pos):
        self.radius = radius
        self.color = color
        self.range = towerRange + radius
        self.damage = damage
        self.last_attack_time = 0
        self.cooldown = cooldown
        self.x_pos = x_pos
        self.y_pos = y_pos


    def draw(self, screen):
        pygame.draw.circle(screen, "gray", (self.x_pos, self.y_pos), radius=self.radius + self.range)
        pygame.draw.circle(screen, self.color, (self.x_pos, self.y_pos), radius=self.radius)

    def attack(self, screen, enemy, distance):

        current_time = pygame.time.get_ticks()

        if distance <= self.range:
            pygame.draw.line(screen, "yellow", (self.x_pos, self.y_pos), (enemy.x, enemy.y))

            if current_time - self.last_attack_time >= self.cooldown:
                enemy.take_damage(self.damage)
                print(enemy.health)

                self.last_attack_time = current_time
