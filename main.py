import pygame
import math
from enemy import Enemy, ClassicEnemy, WaveEnemy
from towers import Tower, Cannon, Machinegun, Missile_Launcher
from player import Player
from button import Button


def obslugaEventow(ui_Buttons, player, towers, waves_data):
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEMOTION:
                if player.preview_tower is not None:
                    player.preview_tower.update_position(event.pos[0], event.pos[1])

            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
                
                if event.button == 3: # Prawy przycisk myszy - anulowanie
                    player.preview_tower = None
                elif event.button == 1: # Tylko lewy przycisk myszy
                    mouse_pos = event.pos
                    clickedOnPanel = False
                    
                    for button in ui_Buttons:
                        
                        if button.is_clicked(mouse_pos):
                            clickedOnPanel = True

                            if button.name == "Cannon" and player.money >= 100:
                                player.preview_tower = Cannon(mouse_pos[0], mouse_pos[1])

                            elif button.name == "Machinegun" and player.money >= 150:
                                player.preview_tower = Machinegun(mouse_pos[0], mouse_pos[1])

                            elif button.name == "Missle_Launcher" and player.money >= 200:
                                player.preview_tower = Missile_Launcher(mouse_pos[0], mouse_pos[1])

                            elif button.name == "UpgradeTower":
                                if player.selectedTower is not None:
                                    if player.selectedTower.level < 3:
                                        if player.money >= player.selectedTower.upgrade_cost:
                                            player.money -= player.selectedTower.upgrade_cost
                                            player.selectedTower.upgrade()

                            elif button.name == "FastForward":
                                player.is_fast_forward = not player.is_fast_forward
                            break
                        
                    if not clickedOnPanel and mouse_pos[0] < 1200:
                        if player.preview_tower is not None:
                            if player.money >= player.preview_tower.cost:
                                player.money -= player.preview_tower.cost
                                towers.append(player.preview_tower)
                            
                            player.preview_tower = None
                            player.selectedTower = None
                        else:
                            # Próba zaznaczenia wieży
                            clicked_tower = None
                            for tower in towers:
                                dist = math.hypot(tower.x_pos - mouse_pos[0], tower.y_pos - mouse_pos[1])
                                if dist < 25: # promień podstawy wieży (ok. 25px)
                                    clicked_tower = tower
                                    break
                            player.selectedTower = clicked_tower
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

    # Przyciski Fast Forward
    ff_off_img = pygame.image.load('Assets/ff_off.png')
    ff_off_img = pygame.transform.smoothscale(ff_off_img, (220, 100))
    ff_on_img = pygame.image.load('Assets/ff_on.png')
    ff_on_img = pygame.transform.smoothscale(ff_on_img, (220, 100))


    # Przyciski zaznaczone
    cannon_on = pygame.image.load('Assets/Cannon_on.png')
    cannon_on = pygame.transform.smoothscale(cannon_on, (80, 90))

    machinegun_on = pygame.image.load('Assets/mg_on.png')
    machinegun_on = pygame.transform.smoothscale(machinegun_on, (80, 90))

    missle_launcher_on = pygame.image.load('Assets/Missle_Launcher_on.png')
    missle_launcher_on = pygame.transform.smoothscale(missle_launcher_on, (80, 90))

    ulepszenie_on = pygame.image.load('Assets/ulepsz_on.png')
    ulepszenie_on = pygame.transform.smoothscale(ulepszenie_on, (273, 67))

    enemy_path = [(7, 780), (48, 756), (91, 733), (151, 714), (192, 691), (234, 676), (275, 661), (316, 642), (351, 606), (347, 562), (310, 534), (281, 505), (270, 476), (279, 447), (300, 424), (330, 412),
     (361, 398), (397, 392), (440, 388), (482, 399), (526, 412), (561, 440), (598, 476), (628, 507), (661, 540), (683, 557), (721, 585), (762, 606), (804, 630), (862, 645), (929, 649), (983, 644), (1036, 621),
      (1057, 597), (1073, 568), (1078, 530), (1054, 497), (1021, 480), (982, 468), (932, 453), (892, 440), (866, 423), (846, 400), (845, 374), (868, 348), (911, 333), (952, 318), (985, 315), (1014, 301),
       (1039, 290), (1058, 280), (1075, 270)]

    ui_Buttons = [
        Button(1220, 392, 80, 90, "Cannon"),
        Button(1312, 392, 80, 90, "Machinegun"),
        Button(1405, 392, 80, 90, "Missle_Launcher"),
        Button(1234, 502, 236, 54, "UpgradeTower"),
        Button(1243, 663, 220, 100, "FastForward")
    ]

    waves_data = [
        {"count": 10, "health": 50, "speed": 2, "reward": 10},
        {"count": 15, "health": 70, "speed": 2, "reward": 10},
        {"count": 20, "health": 100, "speed": 3, "reward": 12},
        {"count": 30, "health": 150, "speed": 3, "reward": 15},
        {"count": 50, "health": 250, "speed": 4, "reward": 20}
    ]

    enemies = []
    last_spawn = pygame.time.get_ticks()

    towers = []
    bullets = []

    player = Player()

    game_time = 0
    last_real_time = pygame.time.get_ticks()

    while running:

        current_real_time = pygame.time.get_ticks()
        delta_time = current_real_time - last_real_time
        last_real_time = current_real_time

        if player.is_paused:
            delta_time = 0
            speed_multiplier = 0
        else:
            if player.is_fast_forward:
                delta_time *= 2
            speed_multiplier = 2 if player.is_fast_forward else 1

        game_time += delta_time
        current_time = game_time

        # Automatyczne uruchamianie nowej fali
        if len(player.active_waves) == 0 and len(enemies) <= 3:
            if player.current_wave < len(waves_data):
                wave_info = waves_data[player.current_wave]
                player.active_waves.append({
                    "info": wave_info,
                    "remaining": wave_info["count"],
                    "last_spawn": current_time
                })
                player.current_wave += 1

        for wave in player.active_waves[:]:
            if wave["remaining"] > 0 and current_time - wave["last_spawn"] > 1000:
                new_enemy = WaveEnemy(enemy_path, wave["info"]["speed"], wave["info"]["health"], wave["info"]["reward"])
                enemies.append(new_enemy)
                wave["remaining"] -= 1
                wave["last_spawn"] = current_time
            if wave["remaining"] <= 0:
                player.active_waves.remove(wave)

        running = obslugaEventow(ui_Buttons, player, towers, waves_data)

        screen.blit(scaledBackground, (0, 0))

        for tower in towers:
            tower.draw(screen)
            if tower == player.selectedTower:
                # Rysowanie okręgu zasięgu dla zaznaczonej wieży
                pygame.draw.circle(screen, (255, 255, 255), (tower.x_pos, tower.y_pos), tower.range, 1)

        # Rysowanie podglądu wieży, jeśli jest wybrana
        if player.preview_tower is not None:
            mouse_pos = pygame.mouse.get_pos()
            # Rysujemy podgląd tylko, jeśli celujemy na mapę (a nie na panel boczny)
            if mouse_pos[0] < 1200:
                player.preview_tower.draw(screen)
                # Okrąg pokazujący zasięg podglądu
                pygame.draw.circle(screen, (255, 255, 255), (player.preview_tower.x_pos, player.preview_tower.y_pos), player.preview_tower.range, 1)

        for enemy in enemies:
            enemy.move_to_checkpoint(speed_multiplier)
            enemy.draw(screen)

            if enemy.health <= 0:
                enemies.remove(enemy)
                player.add_money(enemy.reward)
            elif enemy.goal_index >= len(enemy.path):
                player.lose_health(10)
                enemies.remove(enemy)
                if player.health <= 0:
                    running = False

        for tower in towers:
            tower.attack(enemies, bullets, current_time)
        for bullet in bullets:
            bullet.update(speed_multiplier)
            bullet.draw(screen)
            if bullet.hit == True:
                bullets.remove(bullet)

        # Panel boczny
        screen.blit(scaledPasekPrawo, (1200 , 0))
        player.draw_money(screen, (255, 255, 255))
        player.show_health(screen, (255, 255, 255))
        player.show_notification(screen, current_real_time)

        # Rysowanie podświetlenia Cannon
        if isinstance(player.preview_tower, Cannon):
            screen.blit(cannon_on, (1218, 397))

        # Rysowanie podświetlenia Machinegun
        if isinstance(player.preview_tower, Machinegun):
            screen.blit(machinegun_on, (1312, 400))

        # Rysowanie podświetlenia Missile_Launcher
        if isinstance(player.preview_tower, Missile_Launcher):
            screen.blit(missle_launcher_on, (1406, 400))
        
        # Rysowanie podświetlenia ulepszenia
        if player.selectedTower is not None:
            screen.blit(ulepszenie_on, (1217, 502))

        # Wyświetlanie kosztów wież pod przyciskami (żółty kolor)
        fontTowers = pygame.font.SysFont("Poppins", 20)
        screen.blit(fontTowers.render("100$", True, (255, 215, 0)), (1240, 485))
        screen.blit(fontTowers.render("150$", True, (255, 215, 0)), (1332, 485))
        screen.blit(fontTowers.render("250$", True, (255, 215, 0)), (1425, 485))

        # Dynamiczny tekst na przycisku ulepszenia
        if player.selectedTower is not None:
            if player.selectedTower.level < 3:
                upg_text = f"Ulepsz: {player.selectedTower.upgrade_cost}$"
            else:
                upg_text = "MAX LVL"
        else:
            upg_text = "Wybierz wieze"

        fontUpgrade = pygame.font.SysFont("Poppins", 25)
        upg_img = fontUpgrade.render(upg_text, True, (255, 255, 255))
        screen.blit(upg_img, (1290, 570))

        # Tekst o aktualnej fali
        wave_font = pygame.font.SysFont("Poppins", 30)
        wave_text = wave_font.render(f"Fala: {player.current_wave}/{len(waves_data)}", True, (255, 255, 255))
        screen.blit(wave_text, (1310, 20))


        # Rysowanie przycisku FastForward z grafiki
        if player.is_fast_forward:
            screen.blit(ff_on_img, (1243, 663))
        else:
            screen.blit(ff_off_img, (1243, 663))

        (pygame.display.flip())
        clock.tick(60)    


        # ekran konca gry
        if player.health <= 0:
            screen.fill((0, 0, 0))
            font = pygame.font.SysFont("Poppins", 100)
            img = font.render("PRZEGRALES", True, (255, 0, 0))
            text_rect = img.get_rect(center=(750, 400))
            screen.blit(img, text_rect)
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False

        #ekran wygranej
        elif player.current_wave >= len(waves_data) and len(player.active_waves) == 0 and len(enemies) == 0:
            screen.fill((0, 0, 0))
            font = pygame.font.SysFont("Poppins", 100)
            img = font.render("WYGRALES!", True, (0, 255, 0))
            text_rect = img.get_rect(center=(750, 400))
            screen.blit(img, text_rect)
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False

    

    pygame.quit()




main()