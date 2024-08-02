import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, scale_factor):
        pygame.sprite.Sprite.__init__(self)
        
        self.idle_right_frames = [
            pygame.transform.scale_by(pygame.image.load("player/idle/right/tile000.png"), scale_factor),
            pygame.transform.scale_by(pygame.image.load("player/idle/right/tile001.png"), scale_factor),
            pygame.transform.scale_by(pygame.image.load("player/idle/right/tile002.png"), scale_factor),
            pygame.transform.scale_by(pygame.image.load("player/idle/right/tile003.png"), scale_factor)
            ]
        self.idle_left_frames = [
            pygame.transform.scale_by(pygame.image.load("player/idle/left/tile004.png"), scale_factor),
            pygame.transform.scale_by(pygame.image.load("player/idle/left/tile005.png"), scale_factor),
            pygame.transform.scale_by(pygame.image.load("player/idle/left/tile006.png"), scale_factor),
            pygame.transform.scale_by(pygame.image.load("player/idle/left/tile007.png"), scale_factor)
            ]

        self.x = start_x
        self.y = start_y
        self.y_momentum = 0
        self.jump_momentum = 10

        self.state_frames = self.idle_right_frames
        self.frame_index = 0
        self.image = self.idle_right_frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        
        self.state = "idle_right"

    def update_frame(self, state):
        if self.state == state:
            self.frame_index += 1
            if self.frame_index >= len(self.state_frames):
                self.frame_index = 0
            self.image = self.state_frames[self.frame_index]
        else:
            match state:
                case "idle_right":
                    self.state_frames = self.idle_right_frames
                    self.frame_index = 0
                    self.image = self.state_frames[self.frame_index]
                    self.state = state
                case "idle_left":
                    self.state_frames = self.idle_left_frames
                    self.frame_index = 0
                    self.image = self.state_frames[self.frame_index]
                    self.state = state
                case _:
                    self.state_frames = self.idle_right_frames
                    self.frame_index = 0
                    self.image = self.state_frames[self.frame_index]
                    self.state = "idle_right"

    def momentum(self, is_jumping: bool):
        if self.y > HEIGHT - self.image.get_height():
            self.y_momentum = -self.y_momentum
        elif is_jumping:
            self.y_momentum = -self.jump_momentum
        else:
            self.y_momentum += 0.2

    def test_collisions(self, tiles):
        collisions = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                collisions.append(tile)
        return collisions

    def movement(self, x_change, tiles):
        self.x += x_change
        self.rect.topleft = (self.x, self.y)
        collisions = self.test_collisions(tiles)
        for tile in collisions:
            if x_change > 0:
                self.rect.right = tile.left
            if x_change < 0:
                self.rect.left = tile.right
        self.y += self.y_momentum
        self.rect.topleft = (self.x, self.y)
        collisions = self.test_collisions(tiles)
        for tile in collisions:
            if self.y_momentum > 0:
                self.rect.bottom = tile.top
                self.y_momentum = 0
            if self.y_momentum < 0:
                self.rect.top = tile.bottom
                self.y_momentum = 0

    def update(self, x_change, is_jumping: bool, tiles):
        self.momentum(is_jumping)
        self.movement(x_change, tiles)
