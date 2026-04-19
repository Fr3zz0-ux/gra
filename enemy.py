import pygame
import math

class Enemy:

    # konstruktor
    def __init__(self, path, speed, health, reward, width, height, color):

        # pozycja itd
        self.path = path
        self.speed = speed

        # zmienna pomocnicza zeby wiedziec na ktorym punkcie jestesmy
        self.goal_index = 0


        # ustawiamy wspolrzedne na pierwsze rzeczy z trasy
        self.x, self.y = self.path[self.goal_index]


        self.reward = reward

        # zarzadzanie zyciem
        self.health = health
        self.max_health = health
        self.is_alive = True

        # wyglad
        self.width = width
        self.height = height
        self.color = color

    # funkcja do przemieszczania sie przeciwnika
    def move_to_checkpoint(self):

        if self.goal_index >= len(self.path):
            return True

        goal_x, goal_y = self.path[self.goal_index]

        dx = goal_x - self.x
        dy = goal_y - self.y
        distance = math.hypot(dx, dy)

        if distance <= self.speed:
            self.x = goal_x
            self.y = goal_y
            self.goal_index += 1
        else:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

        return False

    # funkcja zadajaca obrazenia
    def take_damage(self, damage):
            self.health -= damage

    # funkcja rysujaca przeciwnika i jego zycie
    def draw(self, screen):

        if self.is_alive is not True or self.health <= 0:
            return

        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height])


        bar_width = 50
        bar_height = 5

        # centrowanie paska zycia
        bar_x = self.x + (self.width / 2) - (bar_width / 2)
        bar_y = self.y + 25

        # obliczanie jaka czesc paska ma byc zielona
        health_ratio = self.health / self.max_health
        current_bar_width = bar_width * health_ratio

        pygame.draw.rect(screen, "red", [bar_x, bar_y, bar_width, bar_height])
        pygame.draw.rect(screen, "green", [bar_x, bar_y, max(0, current_bar_width), bar_height])

class ClassicEnemy(Enemy):
    def __init__(self, path):
        super().__init__(path, speed = 3, health = 70, reward = 10, width = 20, height = 20, color ="black")