import pygame
import math
from enemy import Enemy, ClassicEnemy
from towers import Tower, Cannon
from player import Player

def main():
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    clock = pygame.time.Clock()
    running = True

    background = pygame.image.load('Assets/tlo_poziom_1.png')

    enemy_path = [(770, 10), (770, 370), (260, 370), (260, 790)]
    enemies_count = 10
    enemies = []
    last_spawn = pygame.time.get_ticks()

    towers = []
    bullets = []

    player = Player(0)

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_pos, y_pos = pygame.mouse.get_pos()
                towers.append(Cannon(x_pos, y_pos))



        screen.blit(background, (0, 0))

        for tower in towers:
            tower.draw(screen)

        for enemy in enemies:
            enemy.move_to_checkpoint()
            enemy.draw(screen)

            for tower in towers:
                distance = math.hypot(enemy.x - tower.x_pos, enemy.y - tower.y_pos)
                tower.attack(enemies, bullets)

            if enemy.health <= 0:
                enemies.remove(enemy)
                player.add_money(enemy.reward)
            elif enemy.move_to_checkpoint() == True:
                player.lose_health(10)
                enemies.remove(enemy)
        for bullet in bullets:
            bullet.update()
            bullet.draw(screen)
            if bullet.hit == True:
                bullets.remove(bullet)

        pygame.draw.rect(screen, "purple", [900, 0, 500, 800])
        player.draw_money(screen, (0, 0, 0))
        player.show_health(screen, (0, 0, 0))

        (pygame.display.flip())
        clock.tick(60)

    pygame.quit()




main()