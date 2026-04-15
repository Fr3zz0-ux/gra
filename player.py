import pygame
import math


class Player:
    def __init__(self, money):

        # Przygotowanie obrazka zycia
        original_health = pygame.image.load("Assets/health.png")
        self.health_image = pygame.transform.scale(original_health, (60, 60))

        # Przygotowanie obrazka pieniedzy
        original_money = pygame.image.load("Assets/money.png")
        self.money_image = pygame.transform.scale(original_money, (60, 60))


        self.money = money
        self.health = 100


    def add_money(self, amount):
        self.money += amount

    def show_health(self,screen, text_col):

        screen.blit(self.health_image, [930, 40])

        font = pygame.font.SysFont("Arial", 40)

        img = font.render(str(self.health), True, text_col)
        screen.blit(img, [1010, 50])

    def lose_health(self, damage):
        self.health -= damage


    def draw_money(self, screen, text_col):
        screen.blit(self.money_image, [930, 130])

        font = pygame.font.SysFont("Arial", 40)

        img = font.render(str(self.money), True, text_col)
        screen.blit(img, [1010, 140])
