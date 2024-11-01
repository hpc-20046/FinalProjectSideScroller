# imports
import random
import pygame
from settings import *
from spirit import SpiritFlame
from ui import AnimatedImage, Item

# player object that handles everything to do with the player
class Player:
    def __init__(self, start_x, start_y, scale_factor, border):

        # put player frames into lists according to its direction and state
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
        self.run_right_frames = [
            pygame.transform.scale_by(pygame.image.load('player/run/right/tile008.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/run/right/tile009.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/run/right/tile010.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/run/right/tile011.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/run/right/tile016.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/run/right/tile017.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/run/right/tile018.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/run/right/tile019.png'), scale_factor)
        ]
        self.run_left_frames = [
            pygame.transform.scale_by(pygame.image.load('player/run/left/tile012.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/run/left/tile013.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/run/left/tile014.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/run/left/tile015.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/run/left/tile020.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/run/left/tile021.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/run/left/tile022.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/run/left/tile023.png'), scale_factor)
        ]
        self.idle_jump_left_frames = pygame.transform.scale_by(pygame.image.load('player/idle_jump/left/tile028.png'), scale_factor)
        self.idle_jump_right_frames = pygame.transform.scale_by(pygame.image.load('player/idle_jump/right/tile024.png'), scale_factor)
        self.run_jump_right_frames = pygame.transform.scale_by(pygame.image.load('player/run_jump/right/tile032.png'), scale_factor)
        self.run_jump_left_frames = pygame.transform.scale_by(pygame.image.load('player/run_jump/left/tile036.png'), scale_factor)
        self.roll_left_frames = [
            pygame.transform.scale_by(pygame.image.load('player/roll/left/tile044.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/roll/left/tile045.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/roll/left/tile046.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/roll/left/tile047.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/roll/left/tile052.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/roll/left/tile053.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/roll/left/tile054.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/roll/left/tile055.png'), scale_factor)
        ]
        self.roll_right_frames = [
            pygame.transform.scale_by(pygame.image.load('player/roll/right/tile040.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/roll/right/tile041.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/roll/right/tile042.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/roll/right/tile043.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/roll/right/tile048.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/roll/right/tile049.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/roll/right/tile050.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/roll/right/tile051.png'), scale_factor)
        ]
        self.hit_right_frames = [
            pygame.transform.scale_by(pygame.image.load('player/hit/right/tile064.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/hit/right/tile065.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/hit/right/tile066.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/hit/right/tile067.png'), scale_factor)
        ]
        self.hit_left_frames = [
            pygame.transform.scale_by(pygame.image.load('player/hit/left/tile068.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/hit/left/tile069.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/hit/left/tile070.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/hit/left/tile071.png'), scale_factor)
        ]
        self.death_left_frames = [
            pygame.transform.scale_by(pygame.image.load('player/death/left/tile076.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/death/left/tile077.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/death/left/tile078.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/death/left/tile079.png'), scale_factor)
        ]
        self.death_right_frames = [
            pygame.transform.scale_by(pygame.image.load('player/death/right/tile072.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/death/right/tile073.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/death/right/tile074.png'), scale_factor),
            pygame.transform.scale_by(pygame.image.load('player/death/right/tile075.png'), scale_factor)
        ]

        # level border variable for ease of access
        self.border = border

        # control variables for the player images
        self.state_frames = self.idle_right_frames
        self.frame_index = 0
        self.image = self.idle_right_frames[self.frame_index]
        self.image_offset = pygame.math.Vector2(-9 * scale_factor, -9 * scale_factor)
        self.state = "idle_right"
        self.temp_state = ""

        # defining the rect of the player
        self.rect = pygame.Rect(start_x, start_y, 13 * scale_factor, 19 * scale_factor)

        # control and spacial booleans
        self.left_key, self.right_key, self.facing_left = False, False, False
        self.is_jumping, self.on_ground = False, False
        self.in_air = False

        # variables to do with movement and physics
        self.gravity = 0.35
        self.friction = -0.12
        self.max_velocity = 4
        self.jump_height = 10
        self.terminal_velocity = 10
        self.speed = 2
        self.current_speed = 4

        # physics vectors
        self.position = pygame.math.Vector2(start_x, start_y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, self.gravity)

        # groups for small visuals
        self.arc = pygame.sprite.Group()
        self.poof = pygame.sprite.Group()
        self.flame = pygame.sprite.Group()
        self.item = pygame.sprite.Group()

        # player stats
        self.damage = 1
        self.strength = 1
        self.spirit = 0
        self.attributes = [0, 0, 0, 0]
        self.equip = [0, 0, 0, 0, 0]
        self.power = False
        self.health_update = False

        # player event variables
        self.time = 0
        self.time_start = 0
        self.death_time_start = 0
        self.cooldown = 1500
        self.dash = False
        self.dashing = False
        self.hit = False
        self.hurt = False
        self.dead = False
        self.death_anim = False
        self.alternate = False
        self.alternate_1 = 6
        self.temp_facing = False
        self.explosion = False
        self.animation = False
        self.animation_counter = 4
        self.door = True
        self.door_opened = False
        self.end_game = False

        # sounds
        self.jump_sound = pygame.mixer.Sound('audio/Jump.wav')
        self.dash_sound = pygame.mixer.Sound('audio/dash.wav')
        self.door_sound = pygame.mixer.Sound('audio/door_open.wav')
        self.death_sound = pygame.mixer.Sound('audio/death.wav')
        

    # draw small visuals and player onto screen based on the camera offset
    def draw(self, display):
        self.arc.draw(display)
        self.flame.draw(display)
        self.item.draw(display)
        self.poof.draw(display)
        display.blit(self.image, (self.rect.x + self.image_offset.x, self.rect.y + self.image_offset.x))

    # update small visuals and player
    def update(self, dt, tiles, spikes, border, camera, inventory, enemies, bar, current_level):
        # get ticks
        self.time = pygame.time.get_ticks()
        # check if dash has ended
        if self.time - self.time_start >= 400:
            self.max_velocity = 4
            self.dash = False
            self.dashing = False

        # update damage based on equipped sword
        match self.equip[4]:
            case 1:
                temp_damage = 2
            case 2:
                temp_damage = 1
            case _:
                temp_damage = 0
        self.damage = self.strength + self.attributes[1] + temp_damage

        # open the door if reached 50 spirit and if door has not already opened
        if self.spirit >= 50 and not self.door_opened:
            self.door = False
            self.door_opened = True
            self.door_sound.play()

        # update speed based on attributes
        if not self.dash and current_level != 8 and current_level != 11:
            self.max_velocity = self.current_speed + (self.attributes[3] / 2)
        elif self.dash:
            self.max_velocity = 10
        else:
            self.max_velocity = 4

        # refill health bar when upgrading health
        if self.health_update:
            self.health_update = False
            bar.amount = bar.total

        # update variables for ease of access
        self.equip = inventory.equip
        self.border = border

        # update small visuals
        self.arc.update(self, enemies, camera)
        self.flame.update(camera, self)
        self.item.update(self, camera, inventory)

        # check movement and collisions when not in inventory
        if not inventory.showing:
            self.horizontal_movement(dt, camera)
            self.check_collisions_x(tiles, spikes)
            if not self.dash:
                if not self.end_game:
                    self.vertical_movement(dt)
                    self.check_collisions_y(tiles, spikes)

        # respawn after a certain amount of time after being dead
        if self.time - self.death_time_start >= 3000 and self.death_anim:
            self.dead = False
            self.death_anim = False
            self.hit = False
            self.hurt = False
            self.respawn(current_level, camera, bar)

        # if health is 0, player is dead
        if bar.amount <= 0:
            self.dead = True

    # calculate player movement on the x-axis
    def horizontal_movement(self, dt, camera):
        # reset acceleration
        self.acceleration.x = 0
        # update acceleration based on key pressed
        if self.left_key:
            self.acceleration.x -= self.speed
        elif self.right_key:
            self.acceleration.x += self.speed
        # apply friction
        self.acceleration.x += self.velocity.x * self.friction
        # using kinematics equations to calculate velocity and change in distance and then capping it
        self.velocity.x += self.acceleration.x * dt
        self.limit_velocity(self.max_velocity)
        self.position.x += self.velocity.x * dt + (self.acceleration.x * 0.5) * (dt * dt)
        # setting the rect pos
        self.rect.x = self.position.x - camera.offset_float

    # calculate the player movement on the y-axis
    def vertical_movement(self, dt):
        # change velocity based on gravity
        self.velocity.y += self.acceleration.y * dt
        # cap velocity
        if self.velocity.y > self.terminal_velocity:
            self.velocity.y = self.terminal_velocity

        # calculate distance changed and set rect pos
        self.position.y += self.velocity.y * dt + (self.acceleration.y * 0.5) * (dt * dt)
        self.rect.bottom = self.position.y

    # handles jumping
    def jump(self):
        # if on the ground, apply upwards velocity
        if self.on_ground:
            self.is_jumping = True
            self.velocity.y -= self.jump_height
            self.on_ground = False
            self.jump_sound.play()

    # limits the velocity
    def limit_velocity(self, max_vel):
        # clamping the velocity to the positive and negative values of max_vel
        self.velocity.x = max(min(max_vel, self.velocity.x), -max_vel)
        # set the velocity to 0 if small enough to stop janky movements
        if abs(self.velocity.x) < 0.01:
            self.velocity.x = 0

    # check for collisions with tiles and spikes
    def get_collisions(self, tiles, spikes):
        hits = []
        impaled = False
        # go through all the tiles and add the ones the player has collided with to a list
        for tile in tiles:
            if self.rect.colliderect(tile):
                hits.append(tile)

        # check for a collision with a spike
        for spike in spikes:
            if self.rect.colliderect(spike):
                impaled = True
                break
        # return collisions
        return hits, impaled

    # checks and corrects collisions on the x-axis
    def check_collisions_x(self, tiles, spikes):
        # get collisions
        collisions, spike = self.get_collisions(tiles, spikes)
        # correct tile collisions based on velocity direction
        for tile in collisions:
            if self.velocity.x > 0:
                # adjusts the position by how much the rect position has changed
                temp_rect = self.rect.x
                self.rect.x = tile.left - self.rect.w
                adjust_factor = self.rect.x - temp_rect
                self.position.x += adjust_factor
                self.position.x = int(self.position.x)

            elif self.velocity.x < 0:
                # adjusts the position by how much the rect position has changed
                temp_rect = self.rect.x
                self.rect.x = tile.right
                adjust_factor = self.rect.x - temp_rect
                self.position.x += adjust_factor
                self.position.x = int(self.position.x) + 1
        # player is dead if they touch a spike
        if spike:
            self.dead = True

    # checks for collisions on the y-axis.
    def check_collisions_y(self, tiles, spikes):
        # these make sure that collisions are reliable
        self.on_ground = False
        self.rect.bottom += 1
        # get all the collisions with tiles and spikes
        collisions, spike = self.get_collisions(tiles, spikes)
        # player is dead if touches a spike
        if spike:
            self.dead = True
        # correct collisions based on velocity.
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

    # handles the dash for the player
    def roll(self):
        # don't dash when the player hasn't unlocked it yet
        if not self.power:
            return

        # don't dash if the cooldown hasn't finished
        if not self.time - self.time_start >= self.cooldown:
            return

        # set the velocity for the dash depending on what way the player if facing
        if self.facing_left:
            self.time_start = self.time
            self.velocity.x -= 10
            self.velocity.y = 0
            self.max_velocity = 10
            self.dash = True
        else:
            self.time_start = self.time
            self.velocity.x += 10
            self.velocity.y = 0
            self.max_velocity = 10
            self.dash = True
        # update the player animation to the roll
        self.update_frame("roll", True, False, "")
        self.dash_sound.play()

    # deals with player animations
    def update_frame(self, state, roll, hit, player_state):
        # if the player is dead, play the die animation
        if self.dead:
            # record the state changes while in this animation to restore it correctly
            self.temp_state = state
            # if this is the first frame of the death animation
            if not self.death_anim:
                self.death_sound.play()
                # set the current frames to the death animation
                if self.facing_left:
                    self.state_frames = self.death_left_frames
                    self.frame_index = 0
                    self.image = self.state_frames[self.frame_index]
                    self.death_anim = True
                    self.rect.bottom = self.position.y
                else:
                    self.state_frames = self.death_right_frames
                    self.frame_index = 0
                    self.image = self.state_frames[self.frame_index]
                    self.death_anim = True
                    self.rect.bottom = self.position.y
                # start the respawn countdown
                self.death_time_start = self.time
            else:
                # if it's not updating the roll or hit animation
                if not roll and not hit:
                    # update every second update for slower animation
                    if self.alternate:
                        # increment the index
                        self.frame_index += 1
                        # if it's the last frame, keep it at that frame.
                        if self.frame_index >= len(self.state_frames):
                            self.frame_index -= 1
                        # set the image to the current frame
                        self.image = self.state_frames[self.frame_index]

                    self.alternate = not self.alternate

        else:
            # if the player is dashing, update the dash animation
            if self.dash:
                # record the state changes while in this animation to restore it correctly
                self.temp_state = state
                # if it's the first frame, set the player frames to the dash animation
                if not self.dashing:
                    if self.facing_left:
                        self.state_frames = self.roll_left_frames
                        self.frame_index = 0
                        self.image = self.state_frames[self.frame_index]
                        self.dashing = True
                    else:
                        self.state_frames = self.roll_right_frames
                        self.frame_index = 0
                        self.image = self.state_frames[self.frame_index]
                        self.dashing = True
                else:
                    # if updating the roll animation
                    if roll:
                        # increment the index
                        self.frame_index += 1
                        # if it's the last frame, keep it at that frame.
                        if self.frame_index >= len(self.state_frames):
                            self.frame_index -= 1
                        # set the image to the current frame
                        self.image = self.state_frames[self.frame_index]
            # if the player has been hit
            elif self.hit:
                # record the state changes while in this animation to restore it correctly
                self.temp_state = state
                # if it's the first frame, set the player frames to the hit animation
                if not self.hurt:
                    if self.facing_left:
                        self.state_frames = self.hit_left_frames
                        self.frame_index = 0
                        self.image = self.state_frames[self.frame_index]
                        self.hurt = True
                    else:
                        self.state_frames = self.hit_right_frames
                        self.frame_index = 0
                        self.image = self.state_frames[self.frame_index]
                        self.hurt = True
                    # store the way the player is facing to compare later
                    self.temp_facing = self.facing_left
                else:
                    # if updating the hit animation
                    if hit:
                        # if the way the player is facing has changed, update the animation to match
                        if self.temp_facing != self.facing_left:
                            if self.facing_left:
                                self.state_frames = self.hit_left_frames
                            else:
                                self.state_frames = self.hit_right_frames
                            self.temp_facing = self.facing_left

                        # increment the image index
                        self.frame_index += 1
                        # if it's the last frame, end the animation
                        if self.frame_index >= len(self.state_frames):
                            self.frame_index -= 1
                            self.hit = False
                            self.hurt = False
                        # set the image to the current frame
                        self.image = self.state_frames[self.frame_index]

            else:
                # if it's not updating the dash or the hit animation
                if not roll and not hit:
                    # if there's something stored in the temp state
                    if not self.temp_state == "":

                        player_state = ""
                        # update the player state based on the temp state
                        match self.temp_state:
                                case "idle_right":
                                    self.state_frames = self.idle_right_frames
                                    self.frame_index = 0
                                    self.state = self.temp_state
                                case "idle_left":
                                    self.state_frames = self.idle_left_frames
                                    self.frame_index = 0
                                    self.state = self.temp_state
                                case "run_right":
                                    self.state_frames = self.run_right_frames
                                    self.frame_index = 0
                                    self.state = self.temp_state
                                case "run_left":
                                    self.state_frames = self.run_left_frames
                                    self.frame_index = 0
                                    self.state = self.temp_state
                                case _:
                                    self.state_frames = self.idle_right_frames
                                    self.frame_index = 0
                                    self.state = "idle_right"
                        # reset the temp state
                        self.temp_state = ""

                    # if the player is in the air, set the frame to the in-air frame
                    if not self.on_ground:
                        if abs(self.velocity.x) > 0:
                            if self.facing_left:
                                self.image = self.run_jump_left_frames
                            else:
                                self.image = self.run_jump_right_frames
                        else:
                            if self.facing_left:
                                self.image = self.idle_jump_left_frames
                            else:
                                self.image = self.idle_jump_right_frames

                        # still update the current state even though the player is in the air
                        match state:
                                case "idle_right":
                                    self.state_frames = self.idle_right_frames
                                    self.frame_index = 0
                                    self.state = state
                                case "idle_left":
                                    self.state_frames = self.idle_left_frames
                                    self.frame_index = 0
                                    self.state = state
                                case "run_right":
                                    self.state_frames = self.run_right_frames
                                    self.frame_index = 0
                                    self.state = state
                                case "run_left":
                                    self.state_frames = self.run_left_frames
                                    self.frame_index = 0
                                    self.state = state
                                case _:
                                    self.state_frames = self.idle_right_frames
                                    self.frame_index = 0
                                    self.state = "idle_right"
                    else:
                        # if the state isn't changing, update the image
                        if self.state == state:
                            self.frame_index += 1
                            # if it's the last frame, repeat
                            if self.frame_index >= len(self.state_frames):
                                self.frame_index = 0
                            # set the image to the current frame
                            self.image = self.state_frames[self.frame_index]
                        else:
                            # update the current frames to the ones the player is changing to
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
                                case "run_right":
                                    self.state_frames = self.run_right_frames
                                    self.frame_index = 0
                                    self.image = self.state_frames[self.frame_index]
                                    self.state = state
                                case "run_left":
                                    self.state_frames = self.run_left_frames
                                    self.frame_index = 0
                                    self.image = self.state_frames[self.frame_index]
                                    self.state = state
                                case _:
                                    self.state_frames = self.idle_right_frames
                                    self.frame_index = 0
                                    self.image = self.state_frames[self.frame_index]
                                    self.state = "idle_right"
        # return the player_state
        return player_state

    # handles respawning after death
    def respawn(self, current_level, camera, bar):

        # if the player is out of health, post the game over event
        if bar.amount == 0:
            bar.amount = bar.total
            pygame.event.post(pygame.event.Event(pygame.USEREVENT + 8))
        else:
            # damage the player as punishment
            bar.damage(10, self)
            # respawn player based on current level
            match current_level:
                case 0:
                    self.position = pygame.math.Vector2(300, HEIGHT / 2 + 200)
                    camera.offset_float = 0
                    self.velocity.y = 0
                case 1:
                    self.position = pygame.math.Vector2(0, HEIGHT / 2 + 200)
                    camera.offset_float = 0
                    self.velocity.y = 0
                case 2:
                    self.position = pygame.math.Vector2(0, HEIGHT / 2 + 200)
                    camera.offset_float = 0
                    self.velocity.y = 0
                case 3:
                    self.position = pygame.math.Vector2(0, HEIGHT / 2 + 240)
                    camera.offset_float = 0
                    self.velocity.y = 0
                case 4:
                    self.position = pygame.math.Vector2(0, HEIGHT / 2 + 240)
                    camera.offset_float = 0
                    self.velocity.y = 0
                case 5:
                    self.position = pygame.math.Vector2(0, HEIGHT / 2 + 200)
                    camera.offset_float = 0
                    self.velocity.y = 0
                case 6:
                    self.position = pygame.math.Vector2(WIDTH - self.rect.w, HEIGHT / 2 + 200)
                    camera.offset_float = WIDTH
                    self.velocity.y = 0
                case 7:
                    self.position = pygame.math.Vector2(400, self.rect.h)
                    camera.offset_float = WIDTH
                    self.velocity.y = 0
                case 8:
                    self.position = pygame.math.Vector2(0, HEIGHT / 2 + 200)
                    camera.offset_float = 0
                    self.velocity.y = 0
                case 9:
                    self.position = pygame.math.Vector2(WIDTH / 2 - 150, HEIGHT)
                    camera.offset_float = 0
                    self.velocity.y = -10
                case 10:
                    self.position = pygame.math.Vector2(870, self.rect.h)
                    camera.offset_float = 0
                    self.velocity.y = 0

    # updates the frame instantly when changing direction instead of waiting for the frame to update
    def turn(self, turning_left, player_state):
        state = "idle_right"
        # if not changing direction, cancel
        if turning_left == self.facing_left:
            return
        # update the player state based on the way the player is turning
        elif not turning_left:
            state = "run_right"
        elif turning_left:
            state = "run_left"

        # update the frame
        player_state = self.update_frame(state, False, False, player_state)

        return player_state

    # handles the attacking animation
    def attack(self):
        # if the player is not already attacking, start attacking
        if not self.arc.sprites():
            # create the slash animation
            self.arc.add(Arc(['misc_assets/slash_fx/tile099.png',
                                        'misc_assets/slash_fx/tile100.png',
                                        'misc_assets/slash_fx/tile101.png',
                                        'misc_assets/slash_fx/tile102.png'], 40, (self.rect.x, self.rect.y), 1, self.facing_left))


# slash animation class. deals with the player attacking system and item drops
class Arc(pygame.sprite.Sprite):
    def __init__(self, frames, interval, pos, scale, facingleft):
        pygame.sprite.Sprite.__init__(self)
        # frames for the slash
        self.right_frames = []
        self.left_frames = []
        for frame in frames:
            self.right_frames.append(pygame.transform.scale(pygame.transform.scale_by(
                pygame.image.load(frame), scale), (96 * scale, 96 * scale + 20)))
            self.left_frames.append(pygame.transform.flip(pygame.transform.scale(pygame.transform.scale_by(
                pygame.image.load(frame), scale), (96 * scale, 96 * scale + 20)), 1, 0))

        # timer variables
        self.interval = interval
        self.timer = 0
        self.timer_start = 0

        # frame index
        self.index = 0
        # storing which way the slash is
        self.facingleft = facingleft

        # position variables
        self.pos = pos
        self.offset_right = pygame.math.Vector2(-10, -20)
        self.offset_left = pygame.math.Vector2(-45, -20)

        # set the frames and offset based on direction the player is facing
        if self.facingleft:
            self.current_frames = self.left_frames
            self.offset = self.offset_left
        else:
            self.current_frames = self.right_frames
            self.offset = self.offset_right

        # set the position
        self.pos = (self.pos[0] + self.offset.x, self.pos[1] + self.offset.y)

        # set the image and rect
        self.image = self.current_frames[self.index]
        self.rect = self.image.get_rect(topleft=self.pos)

        # event booleans
        self.damaged = False
        self.sound_played = False

        # sound effects
        self.attack_sound = pygame.mixer.Sound('audio/slash.wav')
        self.hit_sound = pygame.mixer.Sound('audio/hit.wav')

    # update the slash
    def update(self, player, enemies, camera):
        # update the timer
        self.timer = pygame.time.get_ticks()
        # make sure timer event only activate once
        if self.timer_start == 0:
            self.timer_start = self.timer

        # if the frame interval has passed, update the frame
        if self.timer - self.timer_start > self.interval:
            self.index += 1
            self.timer_start = self.timer
            # if it's the last frame, delete the slash
            if self.index >= len(self.current_frames):
                self.kill()
                self.index = 0
        # set the image and position based on the player pos
        self.image = self.current_frames[self.index]
        self.rect.x = player.rect.x + self.offset.x
        self.rect.y = player.rect.y + self.offset.y

        # check if kit any enemies
        kills = self.check_kill(enemies)
        # damage the enemy and apply knockback
        for kill in kills:
            if not self.damaged:
                kill.health -= player.damage
                self.damaged = True
                kill.knockback(player.facing_left)
                self.hit_sound.play()
                self.sound_played = True

            # if killed the enemy, create a poof animation, and drop a spirit or an item
            if kill.health <= 0:
                kill.kill()
                player.poof.add(AnimatedImage([
                    "misc_assets/smoke_fx/tile252.png",
                    "misc_assets/smoke_fx/tile253.png",
                    "misc_assets/smoke_fx/tile254.png",
                    "misc_assets/smoke_fx/tile255.png",
                    "misc_assets/smoke_fx/tile256.png",
                    "misc_assets/smoke_fx/tile257.png",
                    "misc_assets/smoke_fx/tile258.png",
                    "misc_assets/smoke_fx/tile259.png",
                    "misc_assets/smoke_fx/tile260.png",
                    "misc_assets/smoke_fx/tile261.png",
                    "misc_assets/smoke_fx/tile262.png",
                    "misc_assets/smoke_fx/tile263.png",
                ], (kill.position.x, kill.position.y - kill.rect.h - 10), 1, True, True, camera, False))

                # drop a wooden sword if killed a goblin
                if kill.type == 2:
                    player.item.add(Item((kill.position.x, kill.position.y - kill.rect.h), 3, 1.5))
                # drop more spirit if killed an ogre
                elif kill.type == 3:
                    player.flame.add(SpiritFlame((kill.position.x, kill.position.y - kill.rect.h - 20), 3, (5, 10)))
                    if random.random() <= 0.1:
                        player.item.add(
                            Item((kill.position.x, kill.position.y - kill.rect.h), random.randrange(1, 7), 1.5))
                # everything else
                else:
                    player.flame.add(SpiritFlame((kill.position.x, kill.position.y - kill.rect.h - 20), 3, (1, 3)))
                    if random.random() <= 0.1:
                        player.item.add(Item((kill.position.x, kill.position.y - kill.rect.h), random.randrange(1, 7), 1.5))
        # only play the attack sound once
        if not self.sound_played:
            self.attack_sound.play()
            self.sound_played = True

    # checks for collisions with enemies
    def check_kill(self, enemies):
        hits = []
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                hits.append(enemy)

        return hits

