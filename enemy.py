import pygame

class Enemy():
    def __init__(self, x, y):
        self.rect = pygame.Rect((x, y, 80, 100))