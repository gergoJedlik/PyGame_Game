import pygame
import os


class Player(pygame.sprite.Sprite):
    def __init__(
        self, name: str, width: int, height: int, pos: tuple[int, int]
    ) -> None:
        super().__init__()

        self.x_vel: int = 0
        self.y_vel: int = 0
        self.pos = pos
        self.width = width
        self.height = height
        self.name = name

    def get_sprite(self):
        self.char_surf = pygame.image.load(
            os.path.join("kepek", self.name)
        ).convert_alpha()
        self.char_surf = pygame.transform.rotozoom(self.char_surf, 0, 0.5)
        self.char_rect = self.char_surf.get_rect(center=self.pos)
        return self.char_surf, self.char_rect

    def move(self):
        self.pos[0] += self.x_vel

    def load_sprite_sheets(self, dir1, width, height, direction=False):
        path = os.path.join("Assets", dir1, "Sprites")
        images = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

        all_sprites = {}

        for image in images:
            sprite_sheet = pygame.image.load(os.path.join(path, image)).convert_alpha()

            sprites = []

            for i in range(sprite_sheet.get_width() // width):
                surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
                rect = pygame.Rect(i * width, 0, width, height)
                surface.blit(sprite_sheet, (0, 0), rect)
                sprites.append(pygame.transform.scale2x(surface))

            if direction:
                all_sprites[image.replace(".png", "") + "_right"] = sprites
                all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
            else:
                all_sprites[image.replace(".png", "")] = sprites

        return all_sprites
