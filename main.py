import pygame
import settings as sett
from player import Player
from tiles import Tile, Level
from ui import Healthbar, Display_Name, Text
import os

pygame.init()

def main() -> None:
    screen = pygame.display.set_mode((sett.WIDHT, sett.HEIGHT))
    pygame.display.set_caption("Jatek")
    clock = pygame.time.Clock()
    
    player1: Player = Player("Huntress", 30, sett.HEIGHT-400, 150, 150)
    player2: Player = Player("Samurai", 900, sett.HEIGHT-400, 200, 189, "left")

    UI_Elements = get_UI(player1, player2)

    level = Level(sett.LEVEL_MAP_STR)
    floor = level.get_objects

    bg_dict = draw()
    menu_dict = menu()

    active: bool = False
    win: None|str = None
    running = True
    while running:

        if active is True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and not win:
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
                elif event.type == pygame.KEYDOWN and win:
                    if event.key == pygame.K_SPACE:
                        active, win = new_game(player1, player2, win)


            player1.loop(sett.FPS)
            player2.loop(sett.FPS)


            handle_movement(player1, player2, floor)

            handle_hit(player1, player2)

            win = check_end(player1, player2)

            update(screen, bg_dict, player1, player2, UI_Elements, floor, win)

            clock.tick(sett.FPS)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        active, win = new_game(player1, player2, win)

            screen.fill((0, 0, 0))
            for value in menu_dict.values():
                value.draw(screen)

            pygame.display.update()
    

def menu() -> dict[str, Text]:
    menu_dict: dict[str, Text] = {}

    title_text: Text = Text(128, "GAME NAME")
    title_text.align("center", "center")
    menu_dict["game name"] = title_text

    start_text: Text = Text(32, "PRESS 'SPACE' TO PLAY")
    start_text.align("center", (sett.HEIGHT//10)*9)
    menu_dict['press to play'] = start_text

    return menu_dict

def get_UI(player1: Player, player2: Player) -> dict[str, Healthbar|Display_Name]:
    UI_Elements: dict[str, Healthbar] = {}

    player1_healthbar: Healthbar = Healthbar(47, 67, 366, 31, player1)
    UI_Elements["player1 healthbar"] = player1_healthbar

    player2_healthbar: Healthbar = Healthbar(47, 67, 366, 31, player2, "right")
    UI_Elements["player2 healthbar"] = player2_healthbar

    player1_displayname: Display_Name = Display_Name("Huntress", player1_healthbar)
    UI_Elements["player1 name"] = player1_displayname

    player2_displayname: Display_Name = Display_Name("Samurai", player2_healthbar)
    UI_Elements["player2 name"] = player2_displayname
    return UI_Elements
        

def draw() -> dict[str, tuple[pygame.Surface, pygame.Rect]]:
    bg_dict = {}

    bg_surface = pygame.image.load(os.path.join("Assets", "Tileset", "Background_0.png")).convert()
    bg_surface = pygame.transform.scale(bg_surface, (sett.WIDHT, sett.HEIGHT))
    bg_rect = bg_surface.get_rect(bottomleft=(0, sett.HEIGHT))
    bg_dict["background"] = (bg_surface, bg_rect)

    bg_cemetery = pygame.image.load(os.path.join("Assets", "Tileset", "Background_1.png")).convert_alpha()
    bg_cemetery = pygame.transform.scale(bg_cemetery, (sett.WIDHT, sett.HEIGHT))
    bg_crect = bg_surface.get_rect(bottomleft=(0, sett.HEIGHT+75))
    bg_dict["cemetery"] = (bg_cemetery, bg_crect)

    for placement in range((sett.WIDHT//352)+1):
        if placement == 0:
            bg_grass = pygame.image.load(os.path.join("Assets", "Tileset", "Grass_background_2.png")).convert_alpha()
        else:
            bg_grass = pygame.image.load(os.path.join("Assets", "Tileset", "Grass_background_1.png")).convert_alpha()
        bg_g_rect = bg_grass.get_rect(bottomleft=(352*placement, sett.HEIGHT+30))
        bg_dict[f"grass_{placement}"] = (bg_grass, bg_g_rect)
    
    return bg_dict

def new_game(player1: Player, player2: Player, win):
    if win:
        player1.reset("Huntress", 30, sett.HEIGHT-400, 150, 150)
        player2.reset("Samurai", 900, sett.HEIGHT-400, 200, 189, "left")

    active = True
    win = None
    return active, win

def check_end(player1: Player, player2: Player) -> str|None:
    if player1.P_dead:
        return player2.name.upper()
    elif player2.P_dead:
        return player1.name.upper()
    return None

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
            

def update(screen: pygame.Surface, bg_dict: dict[str, tuple[pygame.Surface, pygame.Rect]], player1: Player, player2: Player, ui_elements: dict[str, Healthbar|Display_Name], floor, winner = None):
    for value in bg_dict.values():
        screen.blit(value[0], value[1])


    # Healthbar Lenght Update
    for element in ui_elements.values():
        if type(element) == Healthbar:
            element.update_width()

    for obj in floor:
        obj.draw(screen)


    # SHOW HITBOXES
       # pygame.draw.rect(screen, (0, 0, 255), obj.collidebox, 5)
    # pygame.draw.rect(screen, (0, 255, 0), player1.hitbox, 3)
    # pygame.draw.rect(screen, (0, 255, 0), player2.hitbox, 3)
    # if player1.attackbox_active:
    # pygame.draw.rect(screen, (255, 0, 0), player1.attackbox, 3)
    # if player2.attackbox_active:
    # pygame.draw.rect(screen, (255, 0, 0), player2.attackbox, 3)
    
    player1.draw(screen)
    player2.draw(screen)

    if not winner:
        for element in ui_elements.values():
            element.draw(screen)
    else:
        winner_text: Text = Text(96, winner + " WON!")
        winner_text.align("center", "center")

        restart_text: Text = Text(32, "PRESS 'SPACE' TO RESTART")
        restart_text.align("center", (sett.HEIGHT//10)*9)

        winner_text.draw(screen)
        restart_text.draw(screen)

    pygame.display.update()

if __name__ == "__main__":
    main()

pygame.quit()