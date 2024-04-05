import pygame
import settings as sett
import os


class Object(pygame.sprite.Sprite):
    def __init__(
        self, x: int, y: int, width: int, height: int, name: None | str = None
    ) -> None:
        super().__init__()
        self.obj_rect: pygame.Rect = pygame.Rect(x, y, width, height)
        self.texture: pygame.Surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, screen: pygame.Surface):
        screen.blit(self.texture, (self.obj_rect.x, self.obj_rect.y))


class Tile(Object):
    def __init__(
        self, x: int, y: int, width: int, height: int, literal: str = "x"
    ) -> None:
        super().__init__(x, y, width, height)
        self.literal = literal
        block = self.get_block(width, height)
        self.texture.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.texture)
        self.collidebox = pygame.Rect(x, y, width, 64)
        self.collidebox.bottomleft = self.obj_rect.bottomleft
        self.coordinates: tuple[int, int] = (x, y)

    def get_block(self, x: int, y: int):
        if self.literal == "x":
            path = os.path.join("Assets", "Tileset", "grass.png")
        elif self.literal == "X":
            path = os.path.join("Assets", "Tileset", "fade.png")
        elif self.literal == "z":
            path = os.path.join("Assets", "Tileset", "dirt.png")
        else:
            path = os.path.join("Assets", "Tileset", "Tiles.png")

        image = pygame.image.load(path).convert_alpha()
        surface = pygame.Surface((x, y), pygame.SRCALPHA)
        if not self.literal:
            rect = pygame.Rect(128, 0, x, y)
        else:
            rect = pygame.Rect(224, 32, x, y)

        surface.blit(image, (0, 0), rect)
        return pygame.transform.scale2x(surface)

    @property
    def get_cords(self) -> tuple[int, int]:
        return self.coordinates


class Platform(Object):
    def __init__(
        self, x: int, y: int, width: int, height: int, last: bool = False
    ) -> None:
        if not last:
            super().__init__(x - width // 2 + 34, y + 35, width, height)
            block = self.get_block(width + 60, height)
            self.collidebox = pygame.Rect(x, y, width, 32)
        else:
            super().__init__(x - width // 2 + 34, y + 35, width + 60, height)
            block = self.get_block(width + 60, height)
            self.collidebox = pygame.Rect(x, y, width + 60, 32)

        self.texture.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.texture)
        self.collidebox.topleft = (
            self.obj_rect.topleft[0],
            self.obj_rect.topleft[1] + 64,
        )
        self.coordinates: tuple[int, int] = (x, y)

    def get_block(self, x: int, y: int):
        path = os.path.join("Assets", "Tileset", "Tiles.png")
        image = pygame.image.load(path).convert_alpha()
        surface = pygame.Surface((x, y), pygame.SRCALPHA)
        rect = pygame.Rect(65, 224, x, y)

        surface.blit(image, (0, 0), rect)
        return pygame.transform.scale2x(surface)


class Level:
    def __init__(self, lvl_map_str: list[str]) -> None:
        self.objects: dict[str, Tile | Platform] = {}
        for line_index, line in enumerate(lvl_map_str):
            for letter_index, letter in enumerate(line):
                if letter == "x":
                    self.objects[f"tile_{line_index}_{letter_index}"] = Tile(
                        letter_index * sett.TILE_WIDTH,
                        min(
                            sett.HEIGHT - sett.TILE_HEIGHT,
                            sett.TILE_HEIGHT * line_index,
                        ),
                        sett.TILE_WIDTH,
                        sett.TILE_HEIGHT,
                        literal="x",
                    )
                if letter == "X":
                    self.objects[f"tile_{line_index}_{letter_index}"] = Tile(
                        letter_index * sett.TILE_WIDTH,
                        min(
                            sett.HEIGHT - sett.TILE_HEIGHT,
                            sett.TILE_HEIGHT * line_index,
                        ),
                        sett.TILE_WIDTH,
                        sett.TILE_HEIGHT,
                        literal="X",
                    )
                if letter == "z":
                    self.objects[f"tile_{line_index}_{letter_index}"] = Tile(
                        letter_index * sett.TILE_WIDTH,
                        min(
                            sett.HEIGHT - sett.TILE_HEIGHT,
                            sett.TILE_HEIGHT * line_index,
                        ),
                        sett.TILE_WIDTH,
                        sett.TILE_HEIGHT,
                        literal="z",
                    )
                if letter == "f":
                    self.objects[f"tile_{line_index}_{letter_index}"] = Tile(
                        letter_index * sett.TILE_WIDTH,
                        min(
                            sett.HEIGHT - sett.TILE_WIDTH, sett.TILE_WIDTH * line_index
                        ),
                        sett.TILE_WIDTH,
                        sett.TILE_WIDTH,
                        literal="f",
                    )
                if letter == "p":
                    self.objects[f"platform_{line_index}_{letter_index}"] = Platform(
                        letter_index * sett.TILE_WIDTH,
                        min(
                            sett.HEIGHT - sett.TILE_HEIGHT,
                            sett.TILE_HEIGHT * line_index,
                        ),
                        sett.TILE_WIDTH,
                        sett.TILE_HEIGHT,
                    )
                if letter == "P":
                    self.objects[f"platform_{line_index}_{letter_index}"] = Platform(
                        letter_index * sett.TILE_WIDTH,
                        min(
                            sett.HEIGHT - sett.TILE_HEIGHT,
                            sett.TILE_HEIGHT * line_index,
                        ),
                        sett.TILE_WIDTH,
                        sett.TILE_HEIGHT,
                        True,
                    )

    @property
    def get_objects(self) -> dict[str, Tile | Platform]:
        return self.objects
