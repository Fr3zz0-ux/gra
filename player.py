import pygame
import math


class Player:
    def __init__(self, money):
        self.money = money
        self.health = 100


    def show_health(self,screen):
        pygame.draw.rect(screen, "green", [950, 20, 200, 25])

    def lose_health(self, damage):
        self.health -= damage
