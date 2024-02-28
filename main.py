import pygame
import settings as sett
from player import Player
import os

pygame.init()

def main() -> None:
    screen = pygame.display.set_mode((sett.WIDHT, sett.HEIGHT))
    pygame.display.set_caption("Jatek")
    clock = pygame.time.Clock()
    
    player = Player("bredket.png", 30, 50, (sett.WIDHT//2, sett.HEIGHT//2))
    player_surf, player_rect = player.get_sprite()
    
    running = True
    while running: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
        clock.tick(sett.FPS)
        
        
        
        bg_surface, bg_rect = draw()
        
        update(screen, bg_surface, bg_rect, player_surf, player_rect)
        

def draw():
    bg_surface = pygame.image.load(os.path.join("kepek", "background.jpg"))
    bg_surface = pygame.transform.rotozoom(bg_surface, 0, 0.34)
    bg_rect = bg_surface.get_rect(bottomleft=(0, sett.HEIGHT))
    return bg_surface, bg_rect

def update(screen, bg_surface, bg_rect, player_surf, player_rect):
    screen.blit(bg_surface, bg_rect)
    screen.blit(player_surf, player_rect)
    
    pygame.display.update()

def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = os.path.join('assets', dir1, dir2)
    images = [f for f in listdir(path) if os.path.isfile(os.path.join(path, f))]

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
            all_sprites[image.replace(".png", "")+ "_right"] = sprites
            all_sprites[image.replace(".png", "")+ "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites

if __name__ == "__main__":
    main()

pygame.quit()