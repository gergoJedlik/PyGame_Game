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
    player2 = Player("Samurai", 830, 50, 200, 189, "left")
    
    running = True
    while running: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not player1.P_attack:
                    player1.attack()
                if event.key == pygame.K_RSHIFT and not player2.P_attack:
                    player2.attack()

        player1.loop(sett.FPS)
        player2.loop(sett.FPS)

        handle_movement(player1, player2)

        handle_hit(player1, player2)

        bg_surface, bg_rect = draw()
        update(screen, bg_surface, bg_rect, player1, player2)


        clock.tick(sett.FPS)
        

def draw():
    bg_surface = pygame.image.load(os.path.join("Assets", "Tileset", "Background_0.png"))
    bg_surface = pygame.transform.scale(bg_surface, (sett.WIDHT, sett.HEIGHT))
    bg_rect = bg_surface.get_rect(bottomleft=(0, sett.HEIGHT))
    return bg_surface, bg_rect

def handle_movement(player1: Player, player2: Player):
    keys = pygame.key.get_pressed()

    player1.x_vel = 0
    player1.y_vel = 0

    player2.x_vel = 0
    player2.y_vel = 0

    if not player1.hit and not player1.P_attack:
        if (keys[pygame.K_a]):
            player1.move_left(sett.PLAYER_VEL)
        if (keys[pygame.K_d]):
            player1.move_right(sett.PLAYER_VEL)

    if not player2.hit and not player2.P_attack:
        if (keys[pygame.K_LEFT]):
            player2.move_left(sett.PLAYER_VEL)
        if (keys[pygame.K_RIGHT]):
            player2.move_right(sett.PLAYER_VEL)

def handle_hit(player1: Player, player2: Player):
    if player1.attackbox_active:
        if player1.attackbox.colliderect(player2.hitbox):
            player2.make_hit(player1.dmg)
            # THE IDEA IS TO KNOCKBACK PLAYER2
            # if player1.direction == "right":
            #     player2.move_right(sett.PLAYER_VEL*8)
            # else:
            #     player2.move_left(sett.PLAYER_VEL*8)

    if player2.attackbox_active:
        if player2.attackbox.colliderect(player1.hitbox):
            player1.make_hit(player2.dmg)
            # THE IDEA IS TO KNOCKBACK PLAYER1
            # if player2.direction == "right":
            #     player1.move_right(sett.PLAYER_VEL*8)
            # else:
            #     player1.move_left(sett.PLAYER_VEL*8)

def update(screen: pygame.Surface, bg_surface, bg_rect, player1: Player, player2: Player):
    screen.blit(bg_surface, bg_rect)

    # --TESTS FOR HITBOXES (uncomment to see)--
    pygame.draw.rect(screen, (0, 255, 0), player1.hitbox, 3)
    pygame.draw.rect(screen, (0, 255, 0), player2.hitbox, 3)
    if player1.attackbox_active:
        pygame.draw.rect(screen, (255, 0, 0), player1.attackbox, 3)
    if player2.attackbox_active:
        pygame.draw.rect(screen, (255, 0, 0), player2.attackbox, 3)
    
    player1.draw(screen)
    player2.draw(screen)

    
    
    pygame.display.update()

if __name__ == "__main__":
    main()

pygame.quit()