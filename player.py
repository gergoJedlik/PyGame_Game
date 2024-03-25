import pygame
import settings as sett
import os


class Player(pygame.sprite.Sprite):
    def __init__(
        self, name: str, x: int, y: int,  width: int, height: int, direction: str = "right"
    ) -> None:
        super().__init__()

        self.SPRITES = self.load_sprite_sheets(name, width, height, True)
        self.GRAV = 1
        self.ANIMATION_DELAY = sett.ANIMATION_DELAY

        self.rect: pygame.Rect = pygame.Rect(x, y, width, height)
        if name == 'Huntress':
            self.hitbox: pygame.Rect = pygame.Rect(x+width+8, y+height-13, 53, height*0.7)
            self.p1_hb_cord = self.hitbox.bottomleft
        else:
            self.hitbox: pygame.Rect = pygame.Rect(x+(width*0.75)+10, y+(height*0.7)-2, 53, height*0.6)
            self.p1_hb_cord = self.hitbox.bottomleft 

        self.x_vel: int|float = 0
        self.current_vel: int|float = 0
        self.y_vel: int|float = 0
        self.width = width
        self.height = height

        self.prev_sprite_sheet = 'None'
        self.animation_count = 0
        self.name = name
        self.direction = direction
        self.sprite_sheet = "Idle"

        self.fall_count = 0
        self.P_jump = False
        self.jump_count = 0
        self.jump_force = -self.GRAV * 22
        
        self.P_dash = False
        self.dash_count = 5 * self.ANIMATION_DELAY
        self.dash_cd = 0

        self.P_dismount = False

        self.knockback_force = sett.PLAYER_VEL_1 * 5
        self.P_knockback = False
        
        self.P_attack = False
        self.attack_count = 1
        if name == 'Huntress':
            self.attackbox: pygame.Rect = pygame.Rect(self.hitbox.centerx, self.hitbox.top, self.hitbox.width*2.5, self.hitbox.height * 1.55)
        else: 
            self.attackbox: pygame.Rect = pygame.Rect(self.hitbox.centerx, self.hitbox.top, self.hitbox.width*3.15, self.hitbox.height * 1.22)
        if direction == 'right':
            self.attackbox.bottomleft = (self.hitbox.centerx, self.hitbox.bottom)
        else: 
            self.attackbox.bottomright = (self.hitbox.centerx, self.hitbox.bottom)
        self.attackbox_active = False

        self.hit = False
        self.hit_count = 0

        self.dead = False
        self.death_count = 0
        self.P_dead = False

        self.hp = 360
        self.dmg = 45

        

    def loop(self, fps: int):
        """Loop functions of player class:
            provides basic player functions and actions.

        Args:
            fps (int): Iteratons per second of pygame loop
        """
        self.check_hp()

        if not self.P_dash:
            self.y_vel += min(18, (self.fall_count / 3) * self.GRAV)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps//2:
            self.hit = False
            self.hit_count = 0

        if self.P_knockback:
            self.knockback()

        if self.P_jump:
            self.jump()

              
        if self.P_dash and self.dash_cd == 0:
            self.dash()
        if self.dash_cd != 0:
            self.P_dash = False 
            self.dash_cd -= 1


        self.fall_count += 1
        self.update_sprite()

    def jump(self):
        self.P_jump = True
        if self.jump_force < 0:
            self.y_vel = self.jump_force
            self.jump_force += self.GRAV 

            self.animation_count = 0
            if self.jump_count == 1:
                self.fall_count = 0
            self.jump_count += 1
        else:
            self.P_jump = False
            self.jump_force = -self.GRAV * 22
            
    def dash(self):
        if self.dash_count > 0:
            self.P_dash = True
            
            self.jump_force = 0
            self.fall_count = 0

            if self.direction == "left":
                if self.name == "Huntress":
                    self.move_left(sett.PLAYER_VEL_1*1.7)
                else:
                    self.move_left(sett.PLAYER_VEL_2*2.4)
            else:
                if self.name == "Huntress":
                    self.move_right(sett.PLAYER_VEL_1*1.7)
                else:
                    self.move_right(sett.PLAYER_VEL_2*2.4)
            self.dash_count -= 1           
        else:
            self.P_dash = False
            self.dash_cd = 90
            self.dash_count = 5 * self.ANIMATION_DELAY
            self.jump_force = -self.GRAV * 22    

    def knockback(self, enemy_dir: None|str = None) -> None:
        self.P_knockback = True
        if enemy_dir:
            self.enemy_dir_const = enemy_dir

        if self.knockback_force > 0:

            if self.enemy_dir_const == "left":
                self.move_left(self.knockback_force)
            else:
                self.move_right(self.knockback_force)

            self.knockback_force -= sett.PLAYER_VEL_1//2 

        else:
            self.P_knockback = False
            self.knockback_force = sett.PLAYER_VEL_1 * 5

    def check_hp(self) -> None:
        if self.hp <= 0:
            self.dead = True

    def update_sprite(self) -> None:
        """Updates currently playing animation.
        """
        attack1_ended = False
        if self.dead:
            self.sprite_sheet = 'Death'
            if self.name == "Huntress" and self.death_count // self.ANIMATION_DELAY == 6:
                self.P_dead = True
            elif self.name == "Samurai" and self.death_count // self.ANIMATION_DELAY == 5:
                self.P_dead = True
            else:
                self.death_count += 1
        elif self.hit:
            self.sprite_sheet = 'Hit'
        elif self.P_attack:
            if self.attack_count == 1:
                self.sprite_sheet = 'Attack1'
            else:
                self.sprite_sheet = 'Attack2'

            if self.animation_count // self.ANIMATION_DELAY >= 4:
                self.attackbox_active = True
        elif self.P_jump:
            self.sprite_sheet = 'Jump'
        elif self.y_vel > self.GRAV * 3:
            self.sprite_sheet = 'Fall'
        elif self.x_vel != 0 and not self.P_dash and not self.P_knockback:
            self.sprite_sheet = 'Run'
        elif self.P_dash and self.dash_cd == 0:
            self.sprite_sheet = 'Dash'
        else:
            self.sprite_sheet = 'Idle'

        # Resets Animation Count When New Animation Begins
        if self.sprite_sheet != self.prev_sprite_sheet:
            if self.prev_sprite_sheet == 'Attack1':
                attack1_ended = True
            self.animation_count = 0
            
        self.prev_sprite_sheet = self.sprite_sheet

        sprite_sheet_name = self.sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        if not self.dead:
            sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        else:
            sprite_index = (self.death_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite: pygame.Surface = sprites[sprite_index]

        if attack1_ended and sprite_index == 0:
            self.attack_count = 2

        self.animation_count += 1

        if self.sprite_sheet != 'Attack1':
            if self.animation_count // self.ANIMATION_DELAY >= len(sprites):
                self.attack_count = 1

        # Animation Counter Resets At The End Of Animations
        if (self.animation_count // self.ANIMATION_DELAY) >= len(sprites):
            self.animation_count = 0
            self.P_attack = False
            self.attackbox_active = False

        self.update_mask()

    def update_mask(self):
        self.rect = self.sprite.get_rect(topleft = (self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)
        
    def attack(self):
        self.P_attack = True

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0
        self.P_dismount = False
        
    def place(self, x: int|None, y: int|None):
        if x:
            self.rect.centerx = x
            self.hitbox.centerx = x
            self.attackbox.centerx = x
         
        if y:       
            self.rect.bottom = y
            self.hitbox.bottom = y
            self.attackbox.bottom = y

    def hit_head(self):
        self.P_jump = False
        self.jump_force = -self.GRAV * 22
        self.count = 0
        self.y_vel *= -1

    def draw(self, window: pygame.Surface, offset_x: int = 0, offset_y: int = 0):
        window.blit(self.sprite, (self.rect.x - offset_x, self.rect.y - offset_y))
    
    def make_hit(self, damage: int):
        if self.hit_count == 0:
            self.hp -= damage
        self.hit_count = 0
        self.hit = True
        
    def move(self, dx: int|float, dy: int|float, test: bool = False):
        if dx != 0 and not test:
            self.current_vel = dx
        if not self.dead:
            self.rect.x += int(dx)
            self.hitbox.x += int(dx)
            self.attackbox.x += int(dx)
            
        self.rect.y += int(dy)
        self.hitbox.y += int(dy)
        self.attackbox.y += int(dy)

    def move_right(self, vel: int|float):
        if self.hitbox.right >= sett.WIDHT:
            self.x_vel = 0
        else:
            self.x_vel = vel
        if self.direction != 'right' and not self.P_knockback and not self.dead:
            self.direction = 'right'
            self.attackbox.bottomleft = (self.hitbox.centerx, self.hitbox.bottom)
            self.animation_count = 0
        
    def move_left(self, vel: int|float):
        if self.hitbox.left <= 0:
            self.x_vel = 0
        else:
            self.x_vel = -vel
        if self.direction != 'left' and not self.P_knockback  and not self.dead:
            self.direction = 'left'
            self.attackbox.bottomright = (self.hitbox.centerx, self.hitbox.bottom)
            self.animation_count = 0

    def flip(self, sprites: list[pygame.Surface]) -> list[pygame.Surface]:
        return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

    def load_sprite_sheets(self, character: str, width: int, height: int, direction: bool = False) -> dict[str, list[pygame.Surface]]:
        """Cuts and loads all spritesheets in given directory then saves it to a dict.

        Args:
            character (str): Name of the character.
            width (int): Width of a single sprite in spritesheet.
            height (int): Hight of a single sprite in spritesheet.
            direction (bool, optional): True if both right and left varients are needed. Defaults to False.

        Returns:
            dict[str, list[pygame.Surface]]: Dict with key of animation_direction and value of list with animation frames.
        """
        path = os.path.join("Assets", character, "Sprites")
        images = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

        all_sprites: dict[str, list[pygame.Surface]] = {}

        for image in images:
            sprite_sheet = pygame.image.load(os.path.join(path, image)).convert_alpha()

            sprites: list[pygame.Surface] = []

            for i in range(sprite_sheet.get_width() // width):
                surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
                rect = pygame.Rect(i * width, 0, width, height)
                surface.blit(sprite_sheet, (0, 0), rect)
                sprites.append(pygame.transform.scale(surface, (375, 375)))

            if direction:
                all_sprites[image.replace(".png", "") + "_right"] = sprites
                all_sprites[image.replace(".png", "") + "_left"] = self.flip(sprites)
            else:
                all_sprites[image.replace(".png", "")] = sprites

        return all_sprites
    
    def reset(self, name: str, x: int, y: int,  width: int, height: int, direction: str = "right"):
        self.__init__(name, x, y, width, height, direction)
        