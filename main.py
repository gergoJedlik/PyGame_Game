import pygame
import settings as sett
from player import Player
from tiles import Tile, Level
import os

pygame.init()

def main() -> None:
    screen = pygame.display.set_mode((sett.WIDHT, sett.HEIGHT))
    pygame.display.set_caption("Jatek")
    clock = pygame.time.Clock()
    
    player1 = Player("Huntress", 30, sett.HEIGHT-400, 150, 150)
    player2 = Player("Samurai", 900, sett.HEIGHT-400, 200, 189, "left")

    level = Level(sett.LEVEL_MAP_STR)
    floor = level.get_objects
    
    running = True
    while running:
         
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not player1.P_attack and not player1.dead:
                    player1.attack()
                if event.key == pygame.K_RSHIFT and not player2.P_attack and not player2.dead:
                    player2.attack()
                if event.key == pygame.K_w and not player1.P_attack and player1.jump_count < 1 and not player1.dead:
                    player1.jump()
                if event.key == pygame.K_UP and not player2.P_attack and player2.jump_count < 1 and not player2.dead:
                    player2.jump()
                if event.key == pygame.K_LSHIFT and not player1.P_attack and player1.dash_cd == 0 and not player1.dead:
                    player1.dash()
                if event.key == pygame.K_MINUS  and not player2.P_attack  and player2.dash_cd == 0 and not player2.dead:
                    player2.dash()
                


        player1.loop(sett.FPS)
        player2.loop(sett.FPS)


        handle_movement(player1, player2, floor)

        handle_hit(player1, player2)

        bg_surface, bg_rect = draw()
        update(screen, bg_surface, bg_rect, player1, player2, floor)


        clock.tick(sett.FPS)
        

def draw():
    bg_surface = pygame.image.load(os.path.join("Assets", "Tileset", "Background_0.png")).convert()
    bg_surface = pygame.transform.scale(bg_surface, (sett.WIDHT, sett.HEIGHT))
    bg_rect = bg_surface.get_rect(bottomleft=(0, sett.HEIGHT))
    return bg_surface, bg_rect


def handle_movement(player1: Player, player2: Player, objects):
    keys = pygame.key.get_pressed()

    handle_vertical_collision(player1, player2, objects, player1.y_vel, player2.y_vel)

    if not player1.P_dash and not player1.P_knockback:
        player1.x_vel = 0
    if not player1.P_jump:
        player1.y_vel = 0

    if not player2.P_dash and not player2.P_knockback:
        player2.x_vel = 0
    if not player2.P_jump:
        player2.y_vel = 0

    if not player1.hit and not player1.P_attack and not player1.P_dash:
        if (keys[pygame.K_a]):
            player1.move_left(sett.PLAYER_VEL_1)
        if (keys[pygame.K_d]):
            player1.move_right(sett.PLAYER_VEL_1)

    if not player2.hit and not player2.P_attack and not player2.P_dash:
        if (keys[pygame.K_LEFT]):
            player2.move_left(sett.PLAYER_VEL_2)
        if (keys[pygame.K_RIGHT]):
            player2.move_right(sett.PLAYER_VEL_2)


def handle_hit(player1: Player, player2: Player):
    if player1.attackbox_active:
        if player1.attackbox.colliderect(player2.hitbox):
            player2.make_hit(player1.dmg)
            player2.knockback(player1.direction)
            # THE IDEA IS TO KNOCKBACK PLAYER2
            # if player1.direction == "right":
            #     player2.move_right(sett.PLAYER_VEL*8)
            # else:
            #     player2.move_left(sett.PLAYER_VEL*8)

    if player2.attackbox_active:
        if player2.attackbox.colliderect(player1.hitbox):
            player1.make_hit(player2.dmg)
            player1.knockback(player2.direction)
            # THE IDEA IS TO KNOCKBACK PLAYER1
            # if player2.direction == "right":
            #     player1.move_right(sett.PLAYER_VEL*8)
            # else:
            #     player1.move_left(sett.PLAYER_VEL*8)
            

def handle_vertical_collision(player1: Player, player2: Player, objects: list[Tile], p1_dy, p2_dy):
    collided_objs = []
    for obj in objects:
        if pygame.Rect.colliderect(player1.hitbox, obj.collidebox):
            if p1_dy > 0:
                player1.move(0, -p1_dy)
                player1.landed()
            elif p1_dy < 0:
                player1.move(0, p1_dy)
                player1.hit_head()

        if pygame.Rect.colliderect(player2.hitbox, obj.collidebox):
            if p2_dy > 0:
                player2.move(0, -p2_dy)
                player2.landed()
            elif p2_dy < 0:
                player2.move(0, p2_dy)
                player2.hit_head()
            
            collided_objs.append(obj)
            

def update(screen: pygame.Surface, bg_surface, bg_rect, player1: Player, player2: Player, floor,):
    screen.blit(bg_surface, bg_rect)

    # Healthbar Lenght Update
    health1_bg = pygame.Rect(47, 67, 366, 31)
    health2_bg = pygame.Rect(0, 0, 366, 31)
    health2_bg.topright = (sett.WIDHT - 47, 67)
    player1_health = pygame.Rect(50, 70, player1.hp, 25)
    player2_health = pygame.Rect(0, 0, player2.hp, 25)
    player2_health.topright = (sett.WIDHT - 50, 70)
    
    player1.display_name[1].bottomleft = health1_bg.topleft
    player1.display_name[1].left += 8
    player1.display_name[1].bottom -= int(6.9) - int(6.9-4.20) * int(6.9/(6.9/3))
    player2.display_name[1].bottomright = health2_bg.topright
    player2.display_name[1].bottom -= int(6.9) - int(6.9-4.20) * int(6.9/(6.9/3))
    player2.display_name[1].left -= 8
    
    screen.blit(player1.display_name[0], player1.display_name[1])
    screen.blit(player2.display_name[0], player2.display_name[1])

    for obj in floor:
        obj.draw(screen)


    # SHOW HITBOXES
    #     pygame.draw.rect(screen, (0, 0, 255), obj.collidebox, 5)
    # pygame.draw.rect(screen, (0, 255, 0), player1.hitbox, 3)
    # pygame.draw.rect(screen, (0, 255, 0), player2.hitbox, 3)
    # # if player1.attackbox_active:
    # pygame.draw.rect(screen, (255, 0, 0), player1.attackbox, 3)
    # # if player2.attackbox_active:
    # pygame.draw.rect(screen, (255, 0, 0), player2.attackbox, 3)
    
    player1.draw(screen)
    player2.draw(screen)

    pygame.draw.rect(screen, (255, 135, 10), health1_bg, border_radius=7)
    pygame.draw.rect(screen, (255, 135, 10), health2_bg, border_radius=7)
    pygame.draw.rect(screen, (255, 0, 0), player1_health)
    pygame.draw.rect(screen, (255, 0, 0), player2_health)


    pygame.display.update()

if __name__ == "__main__":
    main()

pygame.quit()