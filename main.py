import pygame
import settings as sett
from player import Player
import os

pygame.init()

def main() -> None:
    screen = pygame.display.set_mode((sett.WIDHT, sett.HEIGHT))
    pygame.display.set_caption("Jatek")
    clock = pygame.time.Clock()
    
    player1 = Player("Huntress", 30, 50, 150, 150)
    player2 = Player("Samurai", 830, 50, 200, 200, "left")
    
    running = True
    while running: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player1.loop(sett.FPS)
        player2.loop(sett.FPS)

        handle_movement(player1, player2) 
        
        #bg_surface, bg_rect = draw()
        bg_surface, bg_rect = 0, 0
        update(screen, bg_surface, bg_rect, player1, player2)


        clock.tick(sett.FPS)
        

def draw():
    bg_surface = pygame.image.load(os.path.join("kepek", "background.jpg"))
    bg_surface = pygame.transform.rotozoom(bg_surface, 0, 0.34)
    bg_rect = bg_surface.get_rect(bottomleft=(0, sett.HEIGHT))
    return bg_surface, bg_rect

def handle_movement(player1: Player, player2: Player):
    keys = pygame.key.get_pressed()

    player1.x_vel = 0
    player1.y_vel = 0

    player2.x_vel = 0
    player2.y_vel = 0

    if (keys[pygame.K_a]):
        player1.move_left(sett.PLAYER_VEL)
    if (keys[pygame.K_d]):
        player1.move_right(sett.PLAYER_VEL)

    if (keys[pygame.K_LEFT]):
        player2.move_left(sett.PLAYER_VEL)
    if (keys[pygame.K_RIGHT]):
        player2.move_right(sett.PLAYER_VEL)

def update(screen: pygame.Surface, bg_surface, bg_rect, player1: Player, player2: Player):
    #screen.blit(bg_surface, bg_rect)
    screen.fill((255, 255, 255))
    player1.draw(screen)
    player2.draw(screen)
    
    pygame.display.update()

if __name__ == "__main__":
    main()

pygame.quit()