from turtle import position
import pygame
from camera import Camera
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, scale_factor, border):
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
        self.image_offset = pygame.math.Vector2(-27, -27)

        self.border = border

        self.rect = pygame.Rect(0, 0, 13 * scale_factor, 19 * scale_factor)
        #self.rect = self.image.get_rect()
        
        self.state = "idle_right"

        self.LEFT_KEY, self.RIGHT_KEY, self.FACING_LEFT = False, False, False
        self.is_jumping, self.on_ground = False, False

        self.gravity = 0.35
        self.friction = -0.12
        self.max_velocity = 6
        self.jump_height = 10
        self.terminal_velocity = 10

        self.position = pygame.math.Vector2(start_x, start_y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, self.gravity)

    def draw(self, display, camera):
        display.blit(self.image, (self.rect.x + self.image_offset.x, self.rect.y + self.image_offset.x))
        #pygame.draw.rect(display, (255, 255, 255), self.rect, width=1)

    def update(self, dt, tiles, spikes, border, camera):
        #self.border = border
        self.horizontal_movement(dt, camera)
        self.check_collisions_x(tiles, spikes, camera)
        self.vertical_movement(dt, camera)
        self.check_collisions_y(tiles, spikes, camera)

    def horizontal_movement(self, dt, camera):
        self.acceleration.x = 0
        if self.LEFT_KEY:
            self.acceleration.x -= 3
        elif self.RIGHT_KEY:
            self.acceleration.x += 3
        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * dt
        self.limit_velocity(self.max_velocity)
        self.position.x += self.velocity.x * dt + (self.acceleration.x * 0.5) * (dt * dt)
        self.position.x = self.position.x
        self.rect.x = self.position.x# - camera.offset.x

    def vertical_movement(self, dt, camera):
        self.velocity.y += self.acceleration.y * dt
        if self.velocity.y > self.terminal_velocity:
            self.velocity.y = self.terminal_velocity

        self.position.y += self.velocity.y * dt + (self.acceleration.y * 0.5) * (dt * dt)
        self.position.y = self.position.y
        self.rect.bottom = self.position.y# - camera.offset.y

    def jump(self):
        if self.on_ground:
            self.is_jumping = True
            self.velocity.y -= self.jump_height
            self.on_ground = False

    def limit_velocity(self, max_vel):
        self.velocity.x = max(min(max_vel, self.velocity.x), -max_vel)
        if abs(self.velocity.x) < 0.01:
            self.velocity.x = 0

    def get_collisions(self, tiles, spikes):
        hits = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hits.append(tile)
                print("length of hits " + str(len(hits)))
                print("collide")
        return hits

    def check_collisions_x(self, tiles, spikes, camera):
        collisions = self.get_collisions(tiles, spikes)
        for tile in collisions:
            if self.velocity.x > 0:
                self.position.x = tile.left - self.rect.w
                self.rect.x = self.position.x# - camera.offset.x
            elif self.velocity.x < 0:
                self.position.x = tile.right 
                self.rect.x = self.position.x# - camera.offset.x

    def check_collisions_y(self, tiles, spikes, camera):
        self.on_ground = False
        self.rect.bottom += 1
        collisions = self.get_collisions(tiles, spikes)
        for tile in collisions:
            print("tile col" + str(tile))
            if self.velocity.y > 0:
                self.on_ground = True
                self.is_jumping = False
                self.velocity.y = 0
                self.position.y = tile.top
                self.rect.bottom = self.position.y# - camera.offset.y
            elif self.velocity.y < 0:
                self.velocity.y = 0
                self.position.y = tile.bottom + self.rect.h
                self.rect.bottom = self.position.y# - camera.offset.y
        if self.position.y > HEIGHT:
            self.on_ground = True
            self.is_jumping = False
            self.velocity.y = 0
            self.position.y = HEIGHT
            self.rect.bottom = self.position.y
        print(self.position)

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

    def turn(self, turning_left):
        state = "idle_right"
        if turning_left == self.FACING_LEFT:
            return
        elif not turning_left:
            state = "idle_right"
        elif turning_left:
            state = "idle_left"

        self.update_frame(state)
