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

        # Przygotowanie pocisku
        filename = asset_path.split("/")[-1]
        name_only = filename.split(".")[0]
        bullet_path = f"Assets/Bullet_{name_only}.png"
        self.original_bullet = pygame.image.load(bullet_path)
        self.bullet_image = pygame.transform.scale(self.original_bullet, (15, 15))

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

    def attack(self, screen, enemy, distance, bullets_list):
        current_time = pygame.time.get_ticks()

        if distance <= self.range:
            if current_time - self.last_attack_time >= self.cooldown:
                new_bullet = Bullet(
                    image=self.bullet_image,
                    start_x=self.top_rect.centerx,
                    start_y=self.top_rect.centery,
                    target_enemy=enemy,
                    damage=self.damage
                )
                bullets_list.append(new_bullet)

                self.last_attack_time = current_time

class Bullet():
    def __init__(self, image, start_x, start_y, target_enemy, damage):
        self.image = image

        # zapisujemy pozycje jako wektor
        self.pos = pygame.math.Vector2(start_x, start_y)
        self.rect = self.image.get_rect(center=(start_x, start_y))

        # Statystyki
        self.target = target_enemy
        self.damage = damage
        self.speed = 20  # Prędkość lotu pocisku
        self.hit = False  # Flaga informująca czy pocisk trafil

    def update(self):

        # Pobieramy pozycje wroga
        target_position = pygame.math.Vector2(self.target.x, self.target.y)

        # Liczymy wektor kierunku
        direction = target_position - self.pos
        distance = direction.length()

        # Sprawdzamy kolizję (jeśli dystans jest mniejszy niż prędkość, to w tej klatce uderzymy)
        if distance < self.speed:
            self.target.take_damage(self.damage)
            self.hit = True  # Oznaczamy pocisk do usunięcia
        else:
            # Jeśli nie trafiliśmy, ruszamy się w stronę wroga!
            direction.normalize_ip()  # Skracamy wektor do długości 1 (sam kierunek)
            self.pos += direction * self.speed  # Dodajemy prędkość

            # Aktualizujemy prostokąt do rysowania (musi być liczbą całkowitą)
            self.rect.center = (round(self.pos.x), round(self.pos.y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Cannon(Tower):
    def __init__(self, x_pos, y_pos):
        super().__init__(asset_path = "Assets/Cannon.png", scale_x= 35, scale_y = 65 ,towerRange = 100, damage = 30, cooldown = 400, x_pos = x_pos, y_pos = y_pos)