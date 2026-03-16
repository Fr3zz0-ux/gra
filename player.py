import pygame
import math


class Player:
    def __init__(self, money):
        self.money = money
        self.health = 100


    def show_health(self,screen):

        bar_width = 200

        pygame.draw.rect(screen, "red", [950, 20, bar_width, 25])

        health_ratio = self.health / 100
        health_bar = bar_width * health_ratio
        pygame.draw.rect(screen, "green", [950, 20, health_bar, 25])

    def lose_health(self, damage):
        self.health -= damage
