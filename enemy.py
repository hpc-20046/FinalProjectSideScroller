import pygame
from settings import *
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, idle_images, walk_images, pos, scale):
        pygame.sprite.Sprite.__init__(self)
        
        self.idle_images = []
        self.walk_images = []
        for image in idle_images:
            self.idle_images.append(pygame.transform.scale_by(pygame.image.load(image), scale))
        for image in walk_images:
            self.walk_images.append(pygame.transform.scale_by(pygame.image.load(image), scale))
        
        self.current_frames = self.idle_images
        self.index = 0
        self.state = 'idle'
        
        self.image = self.current_frames[self.index]
        self.rect = self.image.get_rect(topleft=pos)
        
        self.current_time = 0
        self.timer_start = 0
        
        self.time_until_state_change = random.randrange(500, 5000)
        
    def update_frame(self):
        self.index += 1
        if self.index >= len(self.current_frames):
            self.index = 0
            
        self.image = self.current_frames[self.index]
        
    def update(self):
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.timer_start >= self.time_until_state_change:
            pass
            