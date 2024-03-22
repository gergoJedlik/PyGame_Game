import pygame
from tiles import Platform, Tile
from player import Player


def collide(player: Player, objects: dict[str, Tile|Platform], dx: int|float) -> Tile|Platform|None:
    if dx == 0:
        return None, None
    player.move(dx, 0, test=True)
    player.update()
    collided_object_r: Tile|Platform|None = None
    collided_object_l: Tile|Platform|None = None
    if dx > 0:
        for obj in objects.values():
            if pygame.Rect.colliderect(player.hitbox, obj.collidebox):
                collided_object_l = obj
                break
    if dx < 0:
        for obj in objects.values():
            if pygame.Rect.colliderect(player.hitbox, obj.collidebox):
                collided_object_r = obj
                break

    player.move(-dx, 0, test=True)
    player.update()
    return collided_object_l, collided_object_r

def handle_vertical_collision(player1: Player, player2: Player, objects: dict[str, Tile|Platform], p1_dy: int|float, p2_dy: int|float):
    
    for key, obj in objects.items():
        if pygame.Rect.colliderect(player1.hitbox, obj.collidebox):
            if p1_dy > 0:
                player1.move(0, -p1_dy)
                player1.landed()
            elif p1_dy < 0 and not "platform" in key:
                player1.move(0, p1_dy)
                player1.hit_head()
            elif p1_dy > 0 and "platform" in key:
                player1.climb_platform(obj)

        if pygame.Rect.colliderect(player2.hitbox, obj.collidebox):
            if p2_dy > 0:
                player2.move(0, -p2_dy)
                player2.landed()
            elif p2_dy < 0 and not "platform" in key:
                player2.move(0, p2_dy)
                player2.hit_head()
            elif p2_dy > 0 and "platform" in key:
                player2.climb_platform(obj)