import pygame
import settings as sett
import os

class Object(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, name: None|str =None) -> None:
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Tile(Object):
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        super().__init__(x, y, width, height)
        block = self.get_block(width, height)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        self.collidebox = pygame.Rect(x, y, width, height//2)
        self.collidebox.bottomleft = self.rect.bottomleft
        self.coordinates: tuple[int, int] = (x, y)

    def get_block(self, x: int, y: int):
        path = os.path.join('Assets', 'Tileset', 'Tiles.png')
        image = pygame.image.load(path).convert_alpha()
        surface = pygame.Surface((x, y), pygame.SRCALPHA)
        rect = pygame.Rect(128, 0, x, y)
        surface.blit(image, (0, 0), rect)
        return pygame.transform.scale2x(surface)
    
    @property
    def get_cords(self) -> tuple[int, int]:
        return self.coordinates

    
class Level:
    def __init__(self, lvl_map_str: list[str]) -> None:
        self.objects: list[Tile] = []
        for line_index, line in enumerate(lvl_map_str):
            for letter_index, letter in enumerate(line):
                if letter == "x":
                    self.objects.append(Tile(letter_index * sett.TILE_WIDTH, min(sett.HEIGHT-sett.TILE_HEIGHT, sett.TILE_HEIGHT * line_index), sett.TILE_WIDTH, sett.TILE_HEIGHT))

    @property
    def get_objects(self) -> list[Tile]:
        return self.objects

        