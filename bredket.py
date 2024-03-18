import pygame
from ui import Img
import os
import settings as sett


class Bredket():
    def __init__(self, width: int, height: int) -> None:
        self.Bredket_img: Img = Img(sett.WIDHT//2, sett.HEIGHT//2, os.path.join("Assets", "bredket.png"), (width, height), True)
        self.width = width
        self.height = height
        self.scale = 0

    def scalce_up(self) -> None:
        self.scale += 1
        self.Bredket_img= Img(sett.WIDHT//2, sett.HEIGHT//2, os.path.join("Assets", "bredket.png"), (int(self.width*(self.scale/100)), int(self.height*(self.scale/100))), True)

    def draw(self, screen: pygame.Surface) -> None:
        self.Bredket_img.draw(screen)