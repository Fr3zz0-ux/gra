import pygame
import math
from enemy import Enemy
from towers import Tower

def main():
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    clock = pygame.time.Clock()
    running = True

    background = pygame.image.load('Grafiki/tlo_poziom_1.png')
    enemy_path = [(770, 10), (770, 370), (260, 370), (260, 790)]

    e1 = Enemy(enemy_path, 1, 100, 20, 20, "red")
    t1 = Tower(50, "blue", 100, 10, 1000,300, 300)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        e1.move_to_checkpoint()
        screen.blit(background, (0, 0))
        t1.draw(screen)
        e1.draw(screen)
        distance = math.hypot(e1.x - t1.x_pos, e1.y - t1.y_pos) - t1.radius
        t1.attack(screen, e1, distance)

        (pygame.display.flip())
        clock.tick(60)

    pygame.quit()




main()