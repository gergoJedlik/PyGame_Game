import pygame
import settings as sett
from player import Player
import os

class UiElement:
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.cords = (x, y)
        self.width_height = (width, height)


class Healthbar(UiElement):
    def __init__(self, x: int, y: int, width: int, height: int, player: Player, orient: str = "left") -> None:
        super().__init__(x, y, width, height)
        self.orient = orient
        self.player = player

        if orient == "left":
            self.health_bg = pygame.Rect(x, y, width, height)
            self.player_health = pygame.Rect(x+3, y+3, player.hp, height-6)
        else:
            self.health_bg = pygame.Rect(0, 0, width, height)
            self.health_bg.topright = (sett.WIDHT - x, y)
            self.player_health = pygame.Rect(0, 0, player.hp, height-6)
            self.player_health.topright = (sett.WIDHT - (x+3), y+3)

    def update_width(self) -> None:
        self.player_health.width = self.player.hp
        if self.orient != "left":
            self.player_health.topright = (sett.WIDHT - (self.cords[0]+3), self.cords[1]+3)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, (255, 135, 10), self.health_bg, border_radius=7)
        pygame.draw.rect(screen, (255, 0, 0), self.player_health)

class Text:
    def __init__(self, font_size: int, text: str) -> None:
        self.font = pygame.font.Font(os.path.join("Assets", "DigitalDisco.ttf"), 32)
        self.text: pygame.Surface = self.font.render(text, True, (255, 255, 255), None)
        self.textRect: pygame.Rect = self.text.get_rect()

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.text, self.textRect)


