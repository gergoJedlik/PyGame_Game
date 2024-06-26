import pygame
import settings as sett
from player import Player
from tiles import Tile, Level, Platform
from collision import collide, handle_vertical_collision
from ui import Healthbar, Display_Name, Text, Img
from bredket import Bredket
import os

pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(0.2)


def main() -> None:
    screen = pygame.display.set_mode((sett.WIDHT, sett.HEIGHT))
    pygame.display.set_caption("Blades of Destiny")
    clock = pygame.time.Clock()
    
    player1: Player = Player("Huntress", 30, sett.HEIGHT-400, 150, 150)
    player2: Player = Player("Samurai", 900, sett.HEIGHT-400, 200, 189, "left")
    secret: Bredket = Bredket(sett.WIDHT, sett.HEIGHT)

    UI_Elements = get_UI(player1, player2)

    level = Level(sett.LEVEL_MAP_STR)
    all_tiles: dict[str, Tile|Platform] = level.get_objects

    bg_dict = get_background()
    menu_dict = get_menu()

    game_phase: str = "Menu"
    prev_game_phase: str|None = None

    active: bool = False
    win: None|str = None
    running = True
    while running:
        if prev_game_phase != game_phase:
            load_music(game_phase, prev_game_phase)

        if active is True:
            if game_phase == "Fight":
                prev_game_phase = game_phase
            game_phase = "Fight"

            for event in pygame.event.get():
                if event.type == pygame.QUIT and (not player1.P_dead or not player2.P_dead):
                    running = False
                if event.type == pygame.KEYDOWN and not win:
                    if event.key == pygame.K_g and not player1.P_attack and not player1.dead:
                        player1.attack()
                    if event.key == pygame.K_RSHIFT and not player2.P_attack and not player2.dead:
                        player2.attack()
                    if event.key == pygame.K_w and not player1.P_attack and player1.jump_count < 1 and not player1.dead:
                        player1.jump()
                    if event.key == pygame.K_UP and not player2.P_attack and player2.jump_count < 1 and not player2.dead:
                        player2.jump()
                    if event.key == pygame.K_h and not player1.P_attack and player1.dash_cd == 0 and not player1.dead:
                        player1.dash()
                    if event.key == pygame.K_MINUS  and not player2.P_attack  and player2.dash_cd == 0 and not player2.dead:
                        player2.dash()
                elif event.type == pygame.KEYDOWN and win:
                    if event.key == pygame.K_ESCAPE:
                        active, win = new_game(player1, player2, win, secret)


            player1.loop(sett.FPS)
            player2.loop(sett.FPS)

            
            handle_vertical_collision(player1, player2, all_tiles, player1.y_vel, player2.y_vel)
            if not win:
                handle_movement(player1, player2, all_tiles)
                

            handle_hit(player1, player2)

            win = check_end(player1, player2)

            update(screen, bg_dict, player1, player2, UI_Elements, all_tiles, secret, win)
                

            clock.tick(sett.FPS)
        else:
            if game_phase == "Menu":
                prev_game_phase = game_phase
            game_phase = "Menu"
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        active, win = new_game(player1, player2, win, secret)
                        pygame.mixer.music.rewind()

            for key, value in menu_dict.items():
                if key == 'press to play' and isinstance(value, Text):
                    value.blink()
                if key == 'press to play' and isinstance(value, Text):
                    value.blink()
                value.draw(screen)

            pygame.display.update()
            
    pygame.quit()

# UI Element Initialization Functions an Methods
def get_menu() -> dict[str, Text|Img]:
    menu_dict: dict[str, Text|Img] = {}

    background: Img = Img(sett.WIDHT//2, sett.HEIGHT//2, os.path.join("Assets", "Tileset", "Background_0.png"), (sett.WIDHT, sett.HEIGHT))
    menu_dict["background"] = background

    bg_building: Img = Img(sett.WIDHT//2, sett.HEIGHT//2+75, os.path.join("Assets", "Tileset", "Background_1.png"), (sett.WIDHT, sett.HEIGHT), True) 
    menu_dict["building"] = bg_building

    title_text: Text = Text(128, "Blades of Destiny", pygame.Color(255, 192, 0), True)
    title_text.align("center", "center")
    menu_dict["game name"] = title_text

    start_text: Text = Text(32, "PRESS 'SPACE' TO PLAY")
    start_text.align("center", (sett.HEIGHT//10)*9)
    menu_dict['press to play'] = start_text

    return menu_dict

def get_UI(player1: Player, player2: Player) -> dict[str, Healthbar|Display_Name]:
    UI_Elements: dict[str, Healthbar|Display_Name] = {}

    player1_healthbar: Healthbar = Healthbar(47, 67, 366, 31, player1)
    UI_Elements["player1 healthbar"] = player1_healthbar

    player2_healthbar: Healthbar = Healthbar(47, 67, 366, 31, player2, "right")
    UI_Elements["player2 healthbar"] = player2_healthbar

    player1_displayname: Display_Name = Display_Name("Huntress", player1_healthbar)
    UI_Elements["player1 name"] = player1_displayname

    player2_displayname: Display_Name = Display_Name("Samurai", player2_healthbar)
    UI_Elements["player2 name"] = player2_displayname
    return UI_Elements

def get_background() -> dict[str, Img]:
    bg_dict: dict[str, Img] = {}

    background: Img = Img(sett.WIDHT//2, sett.HEIGHT//2, os.path.join("Assets", "Tileset", "Background_0.png"), (sett.WIDHT, sett.HEIGHT))
    bg_dict["background"] = background

    bg_building: Img = Img(sett.WIDHT//2, sett.HEIGHT//2+75, os.path.join("Assets", "Tileset", "Background_1.png"), (sett.WIDHT, sett.HEIGHT), True) 
    bg_dict["building"] = bg_building

    for placement in range((sett.WIDHT//352)+1):
        if placement == 0:
            bg_grass: Img = Img(0, sett.HEIGHT+30, os.path.join("Assets", "Tileset", "Grass_background_2.png"), transparent=True, left=True)
        else:
            bg_grass: Img = Img(352*placement, sett.HEIGHT+30, os.path.join("Assets", "Tileset", "Grass_background_1.png"), transparent=True, left=True)
        bg_dict[f"grass_{placement}"] = bg_grass
    return bg_dict

def get_winscreen(winner: str) -> dict[str, Text]:
    winsc_dict: dict[str, Text] = {}

    winner_text: Text = Text(96, winner + " WON!", pygame.Color(255, 192, 0))
    winner_text.align("center", "center")
    winsc_dict["winner text"] = winner_text

    sub_text: Text = Text(32, "but their fight never ends...", thin=True)
    sub_text.align("center", winner_text.textRect.bottom+20)
    winsc_dict["sub text"] = sub_text

    restart_text: Text = Text(32, "PRESS 'ESC' TO RESTART")
    restart_text.align("center", (sett.HEIGHT//10)*9)
    winsc_dict["restart text"] = restart_text
    return winsc_dict

def blit_win(screen: pygame.Surface, win_sc_dict: dict[str, Text], win: str):
    for key, value in win_sc_dict.items():
        if key == "restart text":
            value.blink()
        value.draw(screen)

def secret_seq(screen: pygame.Surface, secret: Bredket):
    secret.scalce_up()
    secret.draw(screen)
    if secret.scale == 150:
         quit()

# End and New Game Methods/Functions
def new_game(player1: Player, player2: Player, win: str|None, secret: Bredket):
    if win:
        player1.reset("Huntress", 30, sett.HEIGHT-400, 150, 150)
        player2.reset("Samurai", 900, sett.HEIGHT-400, 200, 189, "left")

    secret.scale = 0
    active = True
    win = None
    return active, win

def check_end(player1: Player, player2: Player) -> str|None:
    if player1.P_dead:
        return player2.name.upper()
    elif player2.P_dead:
        return player1.name.upper()
    return None

# Game and Player Handling Methods
def handle_movement(player1: Player, player2: Player, objects: dict[str, Tile|Platform]):
    keys = pygame.key.get_pressed()

    h_collide_left, h_collide_right = collide(player1, objects, player1.current_vel * 2)
    if not player1.P_dash and not player1.P_knockback:
        player1.x_vel = 0
    if not player1.P_jump:
        player1.y_vel = 0 

    s_collide_left, s_collide_right = collide(player2, objects, player2.current_vel * 2)
    if not player2.P_dash and not player2.P_knockback:
        player2.x_vel = 0
    if not player2.P_jump:
        player2.y_vel = 0


    if not player1.hit and not player1.P_attack and not player1.P_dash:
        if (keys[pygame.K_a]) and not h_collide_right:
            player1.move_left(sett.PLAYER_VEL_1)
        if (keys[pygame.K_d]) and not h_collide_left:
            player1.move_right(sett.PLAYER_VEL_1)
        if (keys[pygame.K_s]):
            player1.P_dismount = True

    if not player2.hit and not player2.P_attack and not player2.P_dash:
        if (keys[pygame.K_LEFT]) and not s_collide_right:
            player2.move_left(sett.PLAYER_VEL_2)
        if (keys[pygame.K_RIGHT]) and not s_collide_left:
            player2.move_right(sett.PLAYER_VEL_2)
        if (keys[pygame.K_DOWN]):
            player2.P_dismount = True

def handle_hit(player1: Player, player2: Player):
    if player1.attackbox_active:
        if player1.attackbox.colliderect(player2.hitbox):
            if not player2.hit:
                player2.make_hit(player1.dmg)
            player2.knockback(player1.direction)

    if player2.attackbox_active:
        if player2.attackbox.colliderect(player1.hitbox):
            if not player1.hit:
                player1.make_hit(player2.dmg)
            player1.knockback(player2.direction)

# Screen Update Method
def update(screen: pygame.Surface, bg_dict: dict[str, Img], player1: Player, player2: Player, ui_elements: dict[str, Healthbar|Display_Name], floor: dict[str, Tile|Platform], secret: Bredket, winner: None|str = None):
    for value in bg_dict.values():
        value.draw(screen)


    # Healthbar Lenght Update
    for element in ui_elements.values():
        if isinstance(element, Healthbar):
            element.update_width()

    for obj in floor.values():
        obj.draw(screen)


    # SHOW HITBOXES
        # pygame.draw.rect(screen, (0, 0, 255), obj.collidebox, 5)
    # pygame.draw.rect(screen, (0, 255, 0), player1.hitbox, 3)
    # pygame.draw.rect(screen, (0, 255, 0), player2.hitbox, 3)
    # if player1.attackbox_active:
    #     pygame.draw.rect(screen, (255, 0, 0), player1.attackbox, 3)
    # if player2.attackbox_active:
    #     pygame.draw.rect(screen, (255, 0, 0), player2.attackbox, 3)
    
    player1.draw(screen)
    player2.draw(screen)

    if not winner:
        for element in ui_elements.values():
            element.draw(screen)
    else:
        if player1.P_dead and player2.P_dead:
            secret_seq(screen, secret)
        else:
            win_sc_dict: dict[str, Text] = get_winscreen(winner)
            blit_win(screen, win_sc_dict, winner)
            

    pygame.display.update()

def load_music(current_phase: str, prev_phase: str|None) -> None:
    if prev_phase is None:
        pygame.mixer.music.load(os.path.join('Assets', 'Sound', 'Music', 'GAME TITLE MUSIC.mp3'))
        pygame.mixer.music.play(loops=-1, fade_ms=1000)
        return
    
    if current_phase == "Fight":
        pygame.mixer.music.unload()
        pygame.mixer.music.load(os.path.join('Assets', 'Sound', 'Music', 'GAME FIGHT MUSIC.mp3'))
        pygame.mixer.music.play(loops=-1)
    elif current_phase == "Win":
        pygame.mixer.music.unload()
    

