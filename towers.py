import pygame
import math

class Tower:

    def __init__(self, asset_path, scale_x, scale_y, towerRange, damage, cooldown, x_pos, y_pos, cost, bullet_scale_x=15, bullet_scale_y=15):

        self.asset_path = asset_path
        self.scale_x = scale_x
        self.scale_y = scale_y
        
        # Przygotowanie lufy
        self.original_top = pygame.image.load(asset_path)
        self.scaled_top = pygame.transform.scale(self.original_top, (scale_x, scale_y))
        self.top_rect = self.scaled_top.get_rect(center = (x_pos, y_pos -  15))
        self.top_image = self.scaled_top

        # Przygotowanie obrazka
        self.original_base = pygame.image.load("Assets/Tower.png")
        self.base_image = pygame.transform.scale(self.original_base, (50, 50))
        self.base_rect = self.base_image.get_rect(center = (x_pos, y_pos))

        # Przygotowanie pocisku
        filename = asset_path.split("/")[-1]
        name_only = filename.split(".")[0]
        self.bullet_path = f"Assets/Bullet_{name_only}.png"
        self.original_bullet = pygame.image.load(self.bullet_path)
        self.bullet_image = pygame.transform.scale(self.original_bullet, (bullet_scale_x, bullet_scale_y))

        # Statystki
        self.range = towerRange
        self.damage = damage
        self.last_attack_time = 0
        self.cooldown = cooldown
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.is_attacking = False
        self.target = None
        self.level = 1
        self.upgrade_cost = 50
        self.cost = cost

    def update_position(self, x, y):
        self.x_pos = x
        self.y_pos = y
        self.base_rect.center = (x, y)
        self.top_rect.center = (x, y - 15)

    def draw(self, screen):
        screen.blit(self.base_image, self.base_rect)
        screen.blit(self.top_image, self.top_rect)

    def upgrade(self):
        if self.level < 3:
            self.level += 1
            # Zwiększamy statystyki
            self.damage = int(self.damage * 1.5)
            self.range = int(self.range * 1.2)
            
            # Ładujemy nowy asset dla wyższego poziomu
            # Jeśli asset to "Assets/Cannon.png", to level 2 będzie miał "Assets/Cannon2.png"
            base_name = self.asset_path.split(".")[0]
            new_asset_path = f"{base_name}{self.level}.png"
            
            try:
                self.original_top = pygame.image.load(new_asset_path)
                self.scaled_top = pygame.transform.scale(self.original_top, (self.scale_x, self.scale_y))
                # Aktualizujemy top_image i top_rect do bieżącej pozycji wieży
                self.top_image = self.scaled_top
                self.top_rect = self.top_image.get_rect(center=(self.x_pos, self.y_pos - 15))
            except:
                print(f"Brak grafiki dla poziomu {self.level}: {new_asset_path}")
                self.top_rect = self.top_image.get_rect(center=(self.x_pos, self.y_pos - 15))

            # Zwiększamy koszt kolejnego ulepszenia
            self.upgrade_cost = int(self.upgrade_cost * 2)
            return True
        return False

    def attack(self, enemies_list, bullets_list, current_time):

        if self.target is not None:
            if not self.target.is_alive or self.target.health <= 0 or self.target not in enemies_list:
                self.target = None
            else:
                target_center_x = self.target.x + (self.target.width / 2)
                target_center_y = self.target.y + (self.target.height / 2)
                distance = math.hypot(target_center_x - self.x_pos, target_center_y - self.y_pos)
                if distance > self.range:
                    self.target = None

        if self.target is None:
            best_enemy = None
            min_distance = self.range + 1

            for enemy in enemies_list:
                if enemy.health > 0:
                    enemy_center_x = enemy.x + (enemy.width / 2)
                    enemy_center_y = enemy.y + (enemy.height / 2)

                    distance = math.hypot(enemy_center_x - self.x_pos, enemy_center_y - self.y_pos)

                    if distance <= self.range and distance < min_distance:
                        best_enemy = enemy
                        min_distance = distance

            self.target = best_enemy

        if self.target is not None:
            self.is_attacking = True

            target_center_x = self.target.x + (self.target.width / 2)
            target_center_y = self.target.y + (self.target.height / 2)

            dx = target_center_x - self.x_pos
            dy = target_center_y - self.y_pos
            angle_rad = math.atan2(dy, dx)
            angle_deg = math.degrees(-angle_rad) - 90

            self.top_image = pygame.transform.rotate(self.scaled_top, angle_deg)

            base_center = (self.x_pos, self.y_pos)
            offset = pygame.math.Vector2(0, -15)
            rotated_offset = offset.rotate(-angle_deg)

            new_center_x = base_center[0] + rotated_offset.x
            new_center_y = base_center[1] + rotated_offset.y

            self.top_rect = self.top_image.get_rect(center=(new_center_x, new_center_y))

            if current_time - self.last_attack_time >= self.cooldown:
                new_bullet = Bullet(
                    image=self.bullet_image,
                    start_x=self.x_pos,
                    start_y=self.y_pos,
                    target_enemy=self.target,
                    damage=self.damage
                )
                bullets_list.append(new_bullet)
                self.last_attack_time = current_time
        else:
            self.is_attacking = False

class Bullet():
    def __init__(self, image, start_x, start_y, target_enemy, damage):
        self.original_image = image
        self.image = image

        # zapisujemy pozycje jako wektor
        self.pos = pygame.math.Vector2(start_x, start_y)
        self.rect = self.image.get_rect(center=(start_x, start_y))

        # Statystyki
        self.target = target_enemy
        self.damage = damage
        self.speed = 20  # Prędkość lotu pocisku
        self.hit = False  # Flaga informująca czy pocisk trafil

    def update(self, speed_multiplier=1):

        # Pobieramy pozycje wroga
        target_position = pygame.math.Vector2(self.target.x + (self.target.width / 2), self.target.y + (self.target.height / 2))

        # Liczymy wektor kierunku
        direction = target_position - self.pos
        distance = direction.length()

        effective_speed = self.speed * speed_multiplier

        # Sprawdzamy kolizję (jeśli dystans jest mniejszy niż prędkość, to w tej klatce uderzymy)
        if distance < effective_speed:
            self.target.take_damage(self.damage)
            self.hit = True  # Oznaczamy pocisk do usunięcia
        else:
            # Jeśli nie trafiliśmy, ruszamy się w stronę wroga!
            direction.normalize_ip()  # Skracamy wektor do długości 1 (sam kierunek)
            self.pos += direction * effective_speed  # Dodajemy prędkość

            # Obliczanie kąta i obrót pocisku w stronę wroga
            angle_rad = math.atan2(direction.y, direction.x)
            # Odejmujemy 90 stopni bo zazwyczaj assety są zorientowane w górę
            angle_deg = math.degrees(-angle_rad) - 90
            self.image = pygame.transform.rotate(self.original_image, angle_deg)

            # Aktualizujemy prostokąt do rysowania (musi być liczbą całkowitą)
            self.rect = self.image.get_rect(center=(round(self.pos.x), round(self.pos.y)))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Cannon(Tower):
    def __init__(self, x_pos, y_pos):
        super().__init__(asset_path = "Assets/Cannon.png", scale_x= 35, scale_y = 65 ,towerRange = 200, damage = 30, cooldown = 400, x_pos = x_pos, y_pos = y_pos, cost = 100, bullet_scale_x = 15, bullet_scale_y = 15)

class Machinegun(Tower):
    def __init__(self, x_pos, y_pos):
        super().__init__(asset_path = "Assets/MG.png", scale_x= 35, scale_y = 65 ,towerRange = 200, damage = 30, cooldown = 400, x_pos = x_pos, y_pos = y_pos, cost = 150, bullet_scale_x = 8, bullet_scale_y = 8)

class Missile_Launcher(Tower):
    def __init__(self, x_pos, y_pos):
        super().__init__(asset_path = "Assets/Missile_Launcher.png", scale_x= 35, scale_y = 65 ,towerRange = 200, damage = 30, cooldown = 400, x_pos = x_pos, y_pos = y_pos, cost = 250, bullet_scale_x = 15, bullet_scale_y = 35)