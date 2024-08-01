import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, startx, starty):
        pygame.sprite.Sprite.__init__(self)
        
        self.idle_right_frames = [
            pygame.image.load("player/idle/right/tile000.png"),
            pygame.image.load("player/idle/right/tile001.png"),
            pygame.image.load("player/idle/right/tile002.png"),
            pygame.image.load("player/idle/right/tile003.png")
            ]
        self.idle_left_frames = [
            pygame.image.load("player/idle/left/tile004.png"),
            pygame.image.load("player/idle/left/tile005.png"),
            pygame.image.load("player/idle/left/tile006.png"),
            pygame.image.load("player/idle/left/tile007.png")
            ]
        

        self.x = startx
        self.y = starty
        
        self.frame = self.idle_right_frames[0]
        self.rect = self.frame.get_rect()
        self.rect.center = (self.x, self.y)
        
        self.state = "idle_right"