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
            self.idle_left_images.append(pygame.transform.flip(pygame.transform.scale_by(pygame.image.load(image), scale), 1, 0))
        for image in walk_images:
            self.walk_right_images.append(pygame.transform.scale_by(pygame.image.load(image), scale))
            self.walk_left_images.append(pygame.transform.flip(pygame.transform.scale_by(pygame.image.load(image), scale), 1, 0))
        
        self.current_frames = self.idle_right_images
        self.index = 0
        self.state = 'idle'
        
        self.image = self.current_frames[self.index]
        self.rect = self.image.get_rect(topleft=pos)
        self.position = pygame.math.Vector2(pos[0], pos[1])
        
        self.current_time = 0
        self.timer_start = 0
        self.facing_left = True
        
        self.time_until_state_change = random.randrange(500, 5000)

        self.idle_time = pygame.math.Vector2(500, 5000)
        self.walk_time = pygame.math.Vector2(4000, 15000)

        self.movement_speed = 1
        self.velocity = 0
        self.gravity = 0.35
        self.terminal_velocity = 10
        
    def update_frame(self):
        self.index += 1
        if self.index >= len(self.current_frames):
            self.index = 0
            
        self.image = self.current_frames[self.index]

    def change_direction(self):
        self.facing_left = not self.facing_left
        if self.facing_left:
            self.current_frames = self.walk_left_images
            self.index = 0
            self.image = self.current_frames[self.index]
        else:
            self.current_frames = self.walk_right_images
            self.index = 0
            self.image = self.current_frames[self.index]

    def update(self, dt, camera, tiles):
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
                self.time_until_state_change = random.randrange(int(self.walk_time.x), int(self.walk_time.y))
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
                self.time_until_state_change = random.randrange(int(self.idle_time.x), int(self.idle_time.y))

            self.timer_start = self.current_time

        self.x_movement(camera)
        self.x_collisions(tiles)
        self.y_movement(dt)
        self.y_collisions(tiles)

    def y_movement(self, dt):
        self.velocity += self.gravity * dt
        if self.velocity > self.terminal_velocity:
            self.velocity = self.terminal_velocity

        self.position.y += self.velocity * dt + (self.gravity * 0.5) * (dt * dt)
        self.rect.bottom = self.position.y

    def y_collisions(self, tiles):
        self.rect.bottom += 1
        collisions = self.get_collisions(tiles)
        for tile in collisions:
            self.velocity = 0
            self.position.y = tile.top
            self.rect.bottom = self.position.y

    def x_movement(self, camera):
        if self.state == 'walk':
            if self.facing_left:
                self.position.x += -self.movement_speed
            else:
                self.position.x += self.movement_speed

        self.rect.x = self.position.x - camera.offset_float

    def x_collisions(self, tiles):
        collisions = self.get_collisions(tiles)
        if collisions:
            self.change_direction()


    def get_collisions(self, tiles):
        hits = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hits.append(tile)
        return hits
            