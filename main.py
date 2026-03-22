from logging import disable

import pygame
import math
from enemy import Enemy, ClassicEnemy
from towers import Tower
from player import Player

def main():
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    clock = pygame.time.Clock()
    running = True

    background = pygame.image.load('Grafiki/tlo_poziom_1.png')

    enemy_path = [(770, 10), (770, 370), (260, 370), (260, 790)]
    enemies_count = 10
    enemies = []
    last_spawn = pygame.time.get_ticks()

    player = Player(0)
    t1 = Tower(50, "blue", 100, 30, 400,300, 240)

    while running:

        current_time = pygame.time.get_ticks()

        if enemies_count > 0 and current_time - last_spawn > 1000:
            new_enemy = ClassicEnemy(enemy_path)
            enemies.append(new_enemy)

            enemies_count -= 1
            last_spawn = current_time




        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(background, (0, 0))

        t1.draw(screen)

        for enemy in enemies:
            enemy.move_to_checkpoint()
            enemy.draw(screen)
            distance = math.hypot(enemy.x - t1.x_pos, enemy.y - t1.y_pos) - t1.radius
            t1.attack(screen, enemy, distance)
            if enemy.health <= 0:
                enemies.remove(enemy)
                player.add_money(enemy.reward)
            if enemy.move_to_checkpoint() == True:
                player.lose_health(10)
                print(player.health)
                enemies.remove(enemy)

        pygame.draw.rect(screen, "purple", [900, 0, 500, 800])
        player.draw_money(screen, (0, 0, 0))
        player.show_health(screen)

        (pygame.display.flip())
        clock.tick(60)

    pygame.quit()




main()