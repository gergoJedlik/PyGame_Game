import pygame
from fighter import Fighter
from enemy import Enemy

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("RPG")

clock = pygame.time.Clock()
FPS = 60

bg_image = pygame.image.load("Images/bg.png")

def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

fighter_1 = Fighter(200, 310)
enemy = Enemy(700, 310)


run = True
while run:
    clock.tick(FPS)

    draw_bg()

    fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen)

    fighter_1.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()