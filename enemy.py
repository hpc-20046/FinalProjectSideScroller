# imports
import pygame
from settings import *
import random

# a class inheriting from pygame.sprite.Sprite to handle everything to do with enemies
class Enemy(pygame.sprite.Sprite):
    def __init__(self, idle_images, walk_images, pos, scale, health, damage, etype):
        # init pygame.sprite.Sprite
        pygame.sprite.Sprite.__init__(self)
        
        # add all the images passed into the object to a list
        self.idle_right_images = []
        self.idle_left_images = []
        self.walk_right_images = []
        self.walk_left_images = []
        for image in idle_images:
            self.idle_right_images.append(pygame.transform.scale_by(pygame.image.load(image), scale))
            # flip for left facing image
            self.idle_left_images.append(pygame.transform.flip(pygame.transform.scale_by(pygame.image.load(image), scale), 1, 0))
        for image in walk_images:
            self.walk_right_images.append(pygame.transform.scale_by(pygame.image.load(image), scale))
            # flip for left facing image
            self.walk_left_images.append(pygame.transform.flip(pygame.transform.scale_by(pygame.image.load(image), scale), 1, 0))
        
        # variables for enemy animations
        self.current_frames = self.idle_right_images
        self.index = 0
        self.state = 'idle'
        
        # setting the image and rect for the pygame.sprite.Sprite class to draw.
        self.image = self.current_frames[self.index]
        self.rect = self.image.get_rect(topleft=pos)
        self.position = pygame.math.Vector2(pos[0], pos[1])
        
        # declare timer variables for animation lengths
        self.current_time = 0
        self.timer_start = 0
        self.facing_left = random.choice([True, False])
        
        # set a random interval for state change
        self.time_until_state_change = random.randrange(500, 5000)

        # constants for time the enemy walks and idles
        self.idle_time = pygame.math.Vector2(500, 5000)
        self.walk_time = pygame.math.Vector2(4000, 15000)
        
        # declare varibles for movement and physics 
        self.movement_speed = 1
        self.velocity = pygame.math.Vector2(0, 0)
        self.gravity = 0.35
        self.terminal_velocity = 10

        # declare health, damage, and enemy type
        self.health = health
        self.damage = damage
        self.type = etype
    
    # update the enemy image based on the current state
    def update_frame(self):
        self.index += 1
        # if the image index is larger than the length, reset to 0
        if self.index >= len(self.current_frames):
            self.index = 0
        
        # set the image to be drawn
        self.image = self.current_frames[self.index]
    
    # function to handle changing direction when touching a wall or being hit by the player
    def change_direction(self):
        # change facing direction
        self.facing_left = not self.facing_left
        # update current state and images
        if self.facing_left:
            self.current_frames = self.walk_left_images
            self.index = 0
            self.image = self.current_frames[self.index]
        else:
            self.current_frames = self.walk_right_images
            self.index = 0
            self.image = self.current_frames[self.index]
    
    # update enemy state, movement calculations, and player collisions
    def update(self, dt, camera, tiles, bar, player):
        # set the timer variable to current ticks passed
        self.current_time = pygame.time.get_ticks()
        # check if the interval has been passed to change state
        if self.current_time - self.timer_start >= self.time_until_state_change:
            # if idling, start walking
            if self.state == 'idle':
                self.state = 'walk'
                # update state images
                if self.facing_left:
                    self.current_frames = self.walk_left_images
                    self.index = 0
                    self.image = self.current_frames[self.index]
                else:
                    self.current_frames = self.walk_right_images
                    self.index = 0
                    self.image = self.current_frames[self.index]
                # choose new random interval for state change
                self.time_until_state_change = random.randrange(int(self.walk_time.x), int(self.walk_time.y))
            else:
                # if walking, start idling
                self.state = 'idle'
                # update state images
                if self.facing_left:
                    self.current_frames = self.idle_left_images
                    self.index = 0
                    self.image = self.current_frames[self.index]
                else:
                    self.current_frames = self.idle_right_images
                    self.index = 0
                    self.image = self.current_frames[self.index]
                    # choose new random interval for state change   
                self.time_until_state_change = random.randrange(int(self.idle_time.x), int(self.idle_time.y))
            # reset the timer
            self.timer_start = self.current_time
        
        # calculate movement and collisions
        self.x_movement(camera)
        self.x_collisions(tiles)
        self.y_movement(dt)
        self.y_collisions(tiles)

        # check for player collisions
        self.check_player_collisions(bar, player)

    # calculate and move the enemy on the y axis
    def y_movement(self, dt):
        # increase the y velocity based on the gravity 
        self.velocity.y += self.gravity * dt
        # cap the y velocity at the ternimal velocity
        if self.velocity.y > self.terminal_velocity:
            self.velocity.y = self.terminal_velocity

        # using a kinematics equation to calculate the change in distance
        self.position.y += self.velocity.y * dt + (self.gravity * 0.5) * (dt * dt)
        # set the rect position to the calculated position
        self.rect.bottom = self.position.y

    # check and correct the y collisions
    def y_collisions(self, tiles):
        # move the rect down 1 to ensure no jank collisions
        self.rect.bottom += 1
        # get all tile collisions
        collisions = self.get_collisions(tiles)
        # correct position for every tile
        for tile in collisions:
            self.velocity.y = 0
            self.position.y = tile.top
            self.rect.bottom = self.position.y

    # calculate and move the enemy on the x axis
    def x_movement(self, camera):
        # if walking, update the position based on the movement speed and the directiom its facing only if not in knockback animation
        if self.state == 'walk':
            if self.velocity.x == 0:
                if self.facing_left:
                    self.position.x += -self.movement_speed
                else:
                    self.position.x += self.movement_speed

        # increase the position based on the velocity
        self.position.x += self.velocity.x
        # decrease the velocity over time
        if self.velocity.x > 0:
            self.velocity.x -= 1
        elif self.velocity.x < 0:
            self.velocity.x += 1
        elif abs(self.velocity.x) < 2:
            self.velocity.x = 0

        # set the rect position to the position minus the camera offset
        self.rect.x = self.position.x - camera.offset_float

    def x_collisions(self, tiles):
        collisions = self.get_collisions(tiles)
        for tile in collisions:
            if not self.facing_left:
                temp_rect = self.rect.x
                self.rect.x = tile.left - self.rect.w
                adjust_factor = self.rect.x - temp_rect
                self.position.x += adjust_factor
                self.position.x = int(self.position.x) - 1
                self.velocity.x = 0
            elif self.facing_left:
                temp_rect = self.rect.x
                self.rect.x = tile.right
                adjust_factor = self.rect.x - temp_rect
                self.position.x += adjust_factor
                self.position.x = int(self.position.x) + 1
                self.velocity.x = 0

        if collisions:
            self.change_direction()



    def get_collisions(self, tiles):
        hits = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hits.append(tile)
        return hits

    def knockback(self, left):
        if self.facing_left != left:
            self.change_direction()
        self.facing_left = left
        if left:
            self.velocity.x = -15
            self.velocity.y = -5
        else:
            self.velocity.x = 15
            self.velocity.y = -5

    def check_player_collisions(self, bar, player):
        if player.rect.colliderect(self.rect):
            bar.damage(self.damage, player)
            
    
            