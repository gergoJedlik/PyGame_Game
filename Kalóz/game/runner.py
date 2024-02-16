from settings import *
from level import Level
import pygame
import sys
from sys import exit

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('First game')
clock = pygame.time.Clock()
level = Level(level_map, screen)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill('#2B1700')
    level.run()

    pygame.display.update()
    clock.tick(60)
