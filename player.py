import pygame
import math


class Player:
    def __init__(self):

        self.money = 0
        self.health = 100
        self.selectedButton = None

    def add_money(self, amount):
        self.money += amount

    def show_health(self,screen, text_col):

        font = pygame.font.SysFont("Poppins", 50)

        img = font.render(str(self.health), True, text_col)
        screen.blit(img, [1355, 115])

    def lose_health(self, damage):
        self.health -= damage


    def draw_money(self, screen, text_col):

        font = pygame.font.SysFont("Poppins", 50)

        img = font.render(str(self.money), True, text_col)
        screen.blit(img, [1355, 262])
