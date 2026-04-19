import pygame
import math
from enemy import Enemy, ClassicEnemy
from towers import Tower, Cannon, Machinegun, Missile_Launcher
from player import Player
from button import Button


def obslugaEventow(ui_Buttons, player, towers):
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Tylko lewy przycisk myszy
                    mouse_pos = event.pos
                    clickedOnPanel = False
                    
                    for button in ui_Buttons:
                        
                        if button.is_clicked(mouse_pos):
                            clickedOnPanel = True

                            if button.name == "Cannon":
                                player.selectedButton = Cannon

                            elif button.name == "Machinegun":
                                player.selectedButton = Machinegun

                            elif button.name == "Missle_Launcher":
                                player.selectedButton = Missile_Launcher

                            elif button.name == "UpgradeTower":
                                print("Wybrano upgrade tower")

                            elif button.name == "FastForward":
                                print("Wybrano fast forward")

                            elif button.name == "Pause":
                                print("Wybrano pause")
                            
                            break
                        
                    if not clickedOnPanel and mouse_pos[0] < 1200:
                        if player.selectedButton is not None:
                            towers.append(player.selectedButton(mouse_pos[0], mouse_pos[1]))
                            player.selectedButton = None
    return True


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

    ui_Buttons = [
        Button(1220, 392, 80, 90, "Cannon"),
        Button(1312, 392, 80, 90, "Machinegun"),
        Button(1405, 392, 80, 90, "Missle_Launcher"),
        Button(1234, 502, 236, 54, "UpgradeTower"),
        Button(1247, 659, 100, 100, "FastForward"),
        Button(1362, 659, 100, 100, "Pause")
    ]

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

        running = obslugaEventow(ui_Buttons, player, towers)

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
        player.draw_money(screen, (255, 255, 255))
        player.show_health(screen, (255, 255, 255))
        
        for btn in ui_Buttons:
            btn.draw_debug(screen)

        (pygame.display.flip())
        clock.tick(60)

    pygame.quit()




main()