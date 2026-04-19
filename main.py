import pygame
import math
from enemy import Enemy, ClassicEnemy
from towers import Tower, Cannon
from player import Player





def main():
    pygame.init()
    screen = pygame.display.set_mode((1500, 800))
    clock = pygame.time.Clock()
    running = True


    # Tlo
    background = pygame.image.load('Assets/tlo_poziom_1.png')
    scaledBackground = pygame.transform.scale(background, (1200, 800))

    # Pasek prawo
    pasekPrawo = pygame.image.load('Assets/pasek_prawy.png')
    scaledPasekPrawo = pygame.transform.smoothscale(pasekPrawo, (300, 800))

    enemy_path = [(7, 780), (48, 756), (91, 733), (151, 714), (192, 691), (234, 676), (275, 661), (316, 642), (351, 606), (347, 562), (310, 534), (281, 505), (270, 476), (279, 447), (300, 424), (330, 412),
     (361, 398), (397, 392), (440, 388), (482, 399), (526, 412), (561, 440), (598, 476), (628, 507), (661, 540), (683, 557), (721, 585), (762, 606), (804, 630), (862, 645), (929, 649), (983, 644), (1036, 621),
      (1057, 597), (1073, 568), (1078, 530), (1054, 497), (1021, 480), (982, 468), (932, 453), (892, 440), (866, 423), (846, 400), (845, 374), (868, 348), (911, 333), (952, 318), (985, 315), (1014, 301),
       (1039, 290), (1058, 280), (1075, 270)]

    enemies_count = 50
    enemies = []
    last_spawn = pygame.time.get_ticks()

    towers = []
    bullets = []

    player = Player()

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
                #print(x_pos, y_pos)
                towers.append(Cannon(x_pos, y_pos))

        screen.blit(scaledBackground, (0, 0))

        for tower in towers:
            tower.draw(screen)

        for enemy in enemies:
            enemy.move_to_checkpoint()
            enemy.draw(screen)

            if enemy.health <= 0:
                enemies.remove(enemy)
                player.add_money(enemy.reward)
            elif enemy.goal_index >= len(enemy.path):
                player.lose_health(10)
                enemies.remove(enemy)

        for tower in towers:
            tower.attack(enemies, bullets)
        for bullet in bullets:
            bullet.update()
            bullet.draw(screen)
            if bullet.hit == True:
                bullets.remove(bullet)


        # Panel boczny
        screen.blit(scaledPasekPrawo, (1200 , 0))
        player.draw_money(screen, (0, 0, 0))
        player.show_health(screen, (0, 0, 0))

        (pygame.display.flip())
        clock.tick(60)

    pygame.quit()




main()