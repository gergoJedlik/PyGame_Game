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
    def __init__(self, font_size: int, text: str, color: pygame.Color = pygame.Color(255, 255, 255), thin: bool = False) -> None:
        self.color = color
        self.string = text
        self.blink_count = 0
 

        if thin:
            self.font = pygame.font.Font(os.path.join("Assets", "DigitalDisco-Thin.ttf"), font_size)
        else:
            self.font = pygame.font.Font(os.path.join("Assets", "DigitalDisco.ttf"), font_size)
        self.text: pygame.Surface = self.font.render(self.string, True, self.color, None)
        self.textRect: pygame.Rect = self.text.get_rect()

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.text, self.textRect)

    def align(self, x: int|str, y: int|str, x_alignment_point: str|None = None, y_alignment_point: str|None = None) -> None:
        if isinstance(x, str):
            if x == "center":
                self.textRect.centerx = sett.WIDHT//2
            elif x == "left":
                self.textRect.left = 25
            elif x == "right":
                self.textRect.right = sett.WIDHT-25
        else:
            if x_alignment_point == "left" or x_alignment_point == None:
                self.textRect.left = int(x)
            elif x_alignment_point == "right":
                self.textRect.right = int(x)
            elif x_alignment_point == "center":
                self.textRect.centerx = int(x)

        if isinstance(y, str):
            if y == "center":
                self.textRect.centery = sett.HEIGHT//2
            elif y == "top":
                self.textRect.top = 25
            elif y == "bottom":
                self.textRect.bottom = sett.HEIGHT-25
        else:
            if y_alignment_point == "top" or y_alignment_point == None:
                self.textRect.top = int(y)
            elif y_alignment_point == "bottom":
                self.textRect.bottom = int(y)
            elif y_alignment_point == "center":
                self.textRect.centery = int(y)

    def blink(self) -> None:
        if self.blink_count == 90:
            self.text: pygame.Surface = self.font.render(self.string, True, pygame.Color((120, 120, 120)), None)
        if self.blink_count == 180:
            self.text: pygame.Surface = self.font.render(self.string, True, self.color, None)
            self.blink_count = 0
        self.blink_count += 1



class Display_Name(Text):
    def __init__(self, name: str, healthbar: Healthbar) -> None:
        super().__init__(32, name)
        if name == "Huntress":
            self.align(healthbar.health_bg.left+8, healthbar.health_bg.top, "left", "bottom")
        else:
            self.align(healthbar.health_bg.right-8, healthbar.health_bg.top, "right", "bottom")


class Img():
    def __init__(self, x: int, y: int, path: str, scale_size: tuple[int, int]|None = None, transparent: bool = False, left: bool = False) -> None:
        if transparent:
            self.surf: pygame.Surface = pygame.image.load(path).convert_alpha()
        else:
            self.surf: pygame.Surface = pygame.image.load(path).convert()

        if scale_size:
            self.surf = pygame.transform.scale(self.surf, scale_size)

        if left:
            self.rect = self.surf.get_rect(bottomleft=(x, y))
        else:
            self.rect = self.surf.get_rect(center=(x, y))

    def draw(self, screen: pygame.Surface):
        screen.blit(self.surf, self.rect)
        