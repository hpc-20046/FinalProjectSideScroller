import pygame
from settings import *
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, idle_images, walk_images, pos, scale):
        pygame.sprite.Sprite.__init__(self)
        
        self.idle_right_images = []
        self.idle_left_images = []
        self.walk_right_images = []
        self.walk_left_images = []
        for image in idle_images:
            self.idle_right_images.append(pygame.transform.scale_by(pygame.image.load(image), scale))
            self.idle_left_images.append(pygame.transform.flip(pygame.transform.scale_by(pygame.image.load(image), scale), 0, 1))
        for image in walk_images:
            self.walk_right_images.append(pygame.transform.scale_by(pygame.image.load(image), scale))
            self.walk_left_images.append(pygame.transform.flip(pygame.transform.scale_by(pygame.image.load(image), scale), 0, 1))
        
        self.current_frames = self.idle_right_images
        self.index = 0
        self.state = 'idle'
        
        self.image = self.current_frames[self.index]
        self.rect = self.image.get_rect(topleft=pos)
        
        self.current_time = 0
        self.timer_start = 0
        self.facing_left = False
        
        self.time_until_state_change = random.randrange(500, 7000)
        
    def update_frame(self, change_in_direction):
        self.index += 1
        if self.index >= len(self.current_frames):
            self.index = 0
        if change_in_direction:
            self.facing_left = not self.facing_left
            
        self.image = self.current_frames[self.index]
        
    def update(self):
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.timer_start >= self.time_until_state_change:
            if self.state == 'idle':
                self.state = 'walk'
                if self.facing_left:
                    self.current_frames = self.walk_left_images
                    self.index = 0
                    self.image = self.current_frames[self.index]
                else:
                    self.current_frames = self.walk_right_images
                    self.index = 0
                    self.image = self.current_frames[self.index]
            else:
                self.state = 'idle'
                if self.facing_left:
                    self.current_frames = self.idle_left_images
                    self.index = 0
                    self.image = self.current_frames[self.index]
                else:
                    self.current_frames = self.idle_right_images
                    self.index = 0
                    self.image = self.current_frames[self.index]

            self.timer_start = self.current_time
            self.time_until_state_change = random.randrange(500, 5000)
            