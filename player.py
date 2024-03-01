import pygame
import os


class Player(pygame.sprite.Sprite):
    def __init__(
        self, name: str, x: int, y: int,  width: int, height: int, direction = "right"
    ) -> None:
        super().__init__()

        self.SPRITES = self.load_sprite_sheets(name, width, height, True)
        self.GRAV = 1
        self.ANIMATION_DELAY = 4

        self.rect: pygame.Rect = pygame.Rect(x, y, width, height)
        self.hitbox: pygame.Rect = pygame.Rect(x, y , 50, 150)
        self.x_vel: int = 0
        self.y_vel: int = 0
        self.width = width
        self.height = height

        self.prev_sprite_sheet = 'None'
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        
        self.hit = False
        self.hit_count = 0
        
        self.P_attack = False
        self.attack_count = 0

        self.dead = False
        self.death_count = 0

        self.hp = 1000
        self.name = name
        self.direction = direction
        self.sprite_sheet = "Idle"



    def loop(self, fps):
        self.check_hp()
        # self.y_vel += min(1, (self.fall_count / fps) * self.GRAV)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps:
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
            self.attack_count += 1
        elif self.y_vel < 0:
            if self.jump_count == 1:
                self.sprite_sheet = 'Jump'
        elif self.y_vel > self.GRAV * 2:
            self.sprite_sheet = 'Fall'
        elif self.x_vel != 0:
            self.sprite_sheet = 'Run'
        else:
            self.sprite_sheet = 'Idle'

        # Resets Animation Count When New Animation Begins
        if self.sprite_sheet != self.prev_sprite_sheet:
            self.animation_count = 0

        self.prev_sprite_sheet = self.sprite_sheet
    
        sprite_sheet_name = self.sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite: pygame.Surface = sprites[sprite_index]

        self.animation_count += 1

        # Death Animation Stalls On Last Frame
        if self.dead and (self.death_count // self.ANIMATION_DELAY) + 1 > len(sprites):
            self.death_count = len(sprites)

        # Animation Counter Resets At The End Of Animations
        if (self.animation_count // self.ANIMATION_DELAY) >= len(sprites):
            self.animation_count = 0
            self.P_attack = False

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
        self.hit = True
        self.hit_count = 0

    def move(self, dx, dy):
        if not self.P_attack:
            self.rect.x += dx
            self.rect.y += dy

            self.hitbox.x += dx
            self.hitbox.y += dy

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != 'right':
            self.direction = 'right'
            self.animation_count = 0
        
    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != 'left':
            self.direction = 'left'
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
