import pygame
import math


class Player:
    def __init__(self):

        self.money = 300
        self.health = 100
        self.selectedButton = None
        self.selectedTower = None
        self.preview_tower = None
        self.notification_msg = ""
        self.notification_time = 0
        self.is_fast_forward = False
        self.is_paused = False

        self.current_wave = 0
        self.wave_in_progress = False
        self.enemies_to_spawn = 0

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

    def trigger_notification(self, message):
        self.notification_msg = message
        self.notification_time = pygame.time.get_ticks()

    def show_notification(self, screen, current_time):
        if self.notification_msg and current_time - self.notification_time < 2000:
            font = pygame.font.SysFont("Poppins", 20)
            img = font.render(self.notification_msg, True, (255, 0, 0))
            # Wyświetlamy powiadomienia na samym dole panelu bocznego, aby nie nakładały się na nic innego
            screen.blit(img, [1210, 770])
