import pygame
import settings as sett
import os


class Player(pygame.sprite.Sprite):
    def __init__(
        self, name: str, x: int, y: int,  width: int, height: int, direction = "right"
    ) -> None:
        super().__init__()

        self.SPRITES = self.load_sprite_sheets(name, width, height, True)
        self.GRAV = 1
        self.ANIMATION_DELAY = sett.ANIMATION_DELAY

        self.rect: pygame.Rect = pygame.Rect(x, y, width, height)
        if name == 'Huntress':
            self.hitbox: pygame.Rect = pygame.Rect(x+width, y+height-13, 50, height*0.6)
            self.p1_hb_cord = self.hitbox.bottomleft
        else:
            self.hitbox: pygame.Rect = pygame.Rect(x+(width*0.75), y+(height*0.7), 50, height*0.5)
            self.p1_hb_cord = self.hitbox.bottomleft 

        self.x_vel: int = 0
        self.y_vel: int = 0
        self.width = width
        self.height = height

        self.prev_sprite_sheet = 'None'
        self.animation_count = 0
        self.name = name
        self.direction = direction
        self.sprite_sheet = "Idle"

        self.fall_count = 0
        self.jump_count = 0
        
        self.dash = False
        self.dash_count = 7 * self.ANIMATION_DELAY
        
        self.P_attack = False
        self.attack_count = 0
        if name == 'Huntress':
            self.attackbox: pygame.Rect = pygame.Rect(self.hitbox.centerx, self.hitbox.top, self.hitbox.width*2.41, self.hitbox.height * 1.7)
        else: 
            self.attackbox: pygame.Rect = pygame.Rect(self.hitbox.centerx, self.hitbox.top, self.hitbox.width*3.1, self.hitbox.height * 1.36)
        if direction == 'right':
            self.attackbox.bottomleft = (self.hitbox.centerx, self.hitbox.bottom)
        else: 
            self.attackbox.bottomright = (self.hitbox.centerx, self.hitbox.bottom)
        self.attackbox_active = False

        self.hit = False
        self.hit_count = 0

        self.dead = False
        self.death_count = 0

        self.hp = 360
        self.dmg = 45

        



    def loop(self, fps):
        self.check_hp()
        # self.y_vel += min(1, (self.fall_count / fps) * self.GRAV)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps//2:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()

    def check_hp(self):
        if self.hp <= 0:
            self.dead = True

    def update_sprite(self):
        if self.dead:
            self.sprite_sheet = 'Death'
            self.death_count += 1
        elif self.hit:
            self.sprite_sheet = 'Hit'
        elif self.P_attack:
            self.sprite_sheet = 'Attack1'
            if self.animation_count // self.ANIMATION_DELAY > 3:
                    self.attackbox_active = True
        elif self.y_vel < 0:
            if self.jump_count == 1:
                self.sprite_sheet = 'Jump'
        elif self.y_vel > self.GRAV * 2:
            self.sprite_sheet = 'Fall'
        elif self.x_vel != 0:
            self.sprite_sheet = 'Run'
        elif self.dash:
            self.sprite_sheet = 'Dash'
        else:
            self.sprite_sheet = 'Idle'

        # Resets Animation Count When New Animation Begins
        if self.sprite_sheet != self.prev_sprite_sheet:
            self.animation_count = 0
            

        self.prev_sprite_sheet = self.sprite_sheet
    
        sprite_sheet_name = self.sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        if not self.dead:
            sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        else:
            sprite_index = (self.death_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite: pygame.Surface = sprites[sprite_index]

        self.animation_count += 1

        # Animation Counter Resets At The End Of Animations
        if (self.animation_count // self.ANIMATION_DELAY) >= len(sprites):
            self.animation_count = 0
            self.P_attack = False
            self.attackbox_active = False

        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft = (self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)
        
    def attack(self):
        self.P_attack = True

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1


    def draw(self, window: pygame.Surface, offset_x = 0, offset_y = 0):
        window.blit(self.sprite, (self.rect.x - offset_x, self.rect.y - offset_y))
    
    def make_hit(self, damage):
        if self.hit_count == 0:
            self.hp -= damage
        self.hit_count = 0
        self.hit = True
        print(self.hp)
        
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

        self.hitbox.x += dx
        self.hitbox.y += dy

        self.attackbox.x += dx
        self.attackbox.y += dy

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != 'right':
            self.direction = 'right'
            self.attackbox.bottomleft = (self.hitbox.centerx, self.hitbox.bottom)
            self.animation_count = 0
        
    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != 'left':
            self.direction = 'left'
            self.attackbox.bottomright = (self.hitbox.centerx, self.hitbox.bottom)
            self.animation_count = 0

    def flip(self, sprites):
        return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

    def load_sprite_sheets(self, character, width, height, direction=False):
        path = os.path.join("Assets", character, "Sprites")
        images = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

        all_sprites = {}

        for image in images:
            sprite_sheet = pygame.image.load(os.path.join(path, image)).convert_alpha()

            sprites = []

            for i in range(sprite_sheet.get_width() // width):
                surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
                rect = pygame.Rect(i * width, 0, width, height)
                surface.blit(sprite_sheet, (0, 0), rect)
                sprites.append(pygame.transform.scale(surface, (350, 350)))

            if direction:
                all_sprites[image.replace(".png", "") + "_right"] = sprites
                all_sprites[image.replace(".png", "") + "_left"] = self.flip(sprites)
            else:
                all_sprites[image.replace(".png", "")] = sprites

        return all_sprites
