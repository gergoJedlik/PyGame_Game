import pygame
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, name: str, width: int, height: int, pos: tuple[int, int]) -> None:
        super().__init__()
        
        self.x_vel: int = 0
        self.y_vel: int = 0
        self.pos = pos
        self.width = width
        self.height = height
        self.name = name
        
    def get_sprite(self):
        self.char_surf = pygame.image.load(os.path.join("kepek", self.name)).convert_alpha()
        self.char_surf = pygame.transform.rotozoom(self.char_surf, 0, 0.5)
        self.char_rect = self.char_surf.get_rect(center=self.pos)
        return self.char_surf, self.char_rect
    
    def move(self):
        
        