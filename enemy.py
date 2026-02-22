import pygame
import math

class Enemy:

    # konstruktor
    def __init__(self, path, speed, health, width, height, color):

        # pozycja itd
        self.path = path
        self.speed = speed

        # zmienna pomocnicza zeby wiedziec na ktorym punkcie jestesmy
        self.goal_index = 0


        # ustawiamy wspolrzedne na pierwsze rzeczy z trasy
        self.x, self.y = self.path[self.goal_index]

        self.health = health

        # wyglad
        self.width = width
        self.height = height
        self.color = color

    # funkcja do przemieszczania sie przeciwnika
    def move_to_checkpoint(self):

        if self.goal_index == len(self.path):
            return

        goal_x, goal_y = self.path[self.goal_index]

        if self.x < goal_x:
            self.x += self.speed
        elif self.x > goal_x:
            self.x -= self.speed

        if self.y < goal_y:
            self.y += self.speed
        elif self.y > goal_y:
            self.y -= self.speed

        if abs(self.x - goal_x) <= self.speed and abs(self.y - goal_y) <= self.speed:
            self.x = goal_x
            self.y = goal_y

            self.goal_index += 1

    def take_damage(self, damage):
        if self.health > 0:
            self.health -= damage

    # funkcja rysujaca przeciwnika
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height])