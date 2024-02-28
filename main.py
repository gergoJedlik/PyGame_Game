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

                

if __name__ == "__main__":
    main()

pygame.quit()