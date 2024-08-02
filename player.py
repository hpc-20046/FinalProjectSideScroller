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

        self.state_frames = self.idle_right_frames
        self.frame_index = 0
        self.image = self.idle_right_frames[self.frame_index]
        self.rect = self.image.get_rect()
        
        self.state = "idle_right"

        self.LEFT_KEY, self.RIGHT_KEY, self.FACING_LEFT = False, False, False
        self.is_jumping, self.on_ground = False, False

        self.gravity = 0.35
        self.friction = -0.12
        self.max_velocity = 6
        self.jump_height = 20

        self.position = pygame.math.Vector2(start_x, start_y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, self.gravity)

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

    def draw(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, dt, tiles):
        self.horizontal_movement(dt)
        self.check_collisions_x(tiles)
        self.vertical_movement(dt)
        self.check_collisions_y(tiles)

    def horizontal_movement(self, dt):
        self.acceleration.x = 0
        if self.LEFT_KEY:
            self.acceleration.x -= 3
        elif self.RIGHT_KEY:
            self.acceleration.x += 3
        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * dt
        self.limit_velocity(self.max_velocity)
        self.position.x += self.velocity.x * dt + (self.acceleration.x * 0.5) * (dt * dt)
        self.rect.x = self.position.x
        print(self.velocity)

    def vertical_movement(self, dt):
        self.velocity.y += self.acceleration.y * dt
        if self.velocity.y > 7:
            self.velocity.y = 7

        self.position.y += self.velocity.y * dt + (self.acceleration.y * 0.5) * (dt * dt)

        self.rect.bottom = self.position.y

    def jump(self):
        if self.on_ground:
            self.is_jumping = True
            self.velocity.y -= self.jump_height
            self.on_ground = False

    def limit_velocity(self, max_vel):
        self.velocity.x = max(min(max_vel, self.velocity.x), -max_vel)
        if abs(self.velocity.x) < 0.01:
            self.velocity.x = 0

    def get_collisions(self, tiles):
        hits = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hits.append(tile)
        return hits

    def check_collisions_x(self, tiles):
        collisions = self.get_collisions(tiles)
        for tile in collisions:
            if self.velocity.x > 0:
                self.position.x = tile.left - self.rect.w
                self.rect.x = self.position.x
            elif self.velocity.x < 0:
                self.position.x = tile.right
                self.rect.x = self.position.x

    def check_collisions_y(self, tiles):
        self.on_ground = False
        self.rect.bottom += 1
        collisions = self.get_collisions(tiles)
        for tile in collisions:
            if self.velocity.y > 0:
                self.on_ground = True
                self.is_jumping = False
                self.velocity.y = 0
                self.position.y = tile.top
                self.rect.bottom = self.position.y
            elif self.velocity.y < 0:
                self.velocity.y = 0
                self.position.y = tile.bottom + self.rect.h
                self.rect.bottom = self.position.y
