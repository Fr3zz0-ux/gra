from logging import disable

import pygame
import math
from enemy import Enemy
from towers import Tower
from player import Player

def main():
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    clock = pygame.time.Clock()
    running = True

    background = pygame.image.load('Grafiki/tlo_poziom_1.png')
    enemy_path = [(770, 10), (770, 370), (260, 370), (260, 790)]

    enemies = [Enemy(enemy_path, 1, 70, 20, 20, "red")]

    player = Player(0)
    t1 = Tower(50, "blue", 100, 15, 1000,300, 240)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        for enemy in enemies:
            enemy.move_to_checkpoint()

        screen.blit(background, (0, 0))

        t1.draw(screen)

        for enemy in enemies:
            enemy.draw(screen)
            distance = math.hypot(enemy.x - t1.x_pos, enemy.y - t1.y_pos) - t1.radius
            #t1.attack(screen, enemy, distance)
            if enemy.move_to_checkpoint() == True:
                player.lose_health(10)
                print(player.health)
                enemies.remove(enemy)

        pygame.draw.rect(screen, "purple", [900, 0, 500, 800])
        player.show_health(screen)

        (pygame.display.flip())
        clock.tick(60)

    pygame.quit()




main()