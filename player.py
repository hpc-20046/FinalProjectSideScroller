import pygame
from settings import *
from ui import AnimatedImage


class Player:
    def __init__(self, start_x, start_y, scale_factor, border):
        
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

        self.state_frames = self.idle_right_frames
        self.frame_index = 0
        self.image = self.idle_right_frames[self.frame_index]
        self.image_offset = pygame.math.Vector2(-9 * scale_factor, -9 * scale_factor)
        self.border = border

        self.rect = pygame.Rect(start_x, start_y, 13 * scale_factor, 19 * scale_factor)
        
        self.state = "idle_right"

        self.LEFT_KEY, self.RIGHT_KEY, self.FACING_LEFT = False, False, False
        self.is_jumping, self.on_ground = False, False
        self.in_air = False

        self.gravity = 0.35
        self.friction = -0.12
        self.max_velocity = 4
        self.jump_height = 10
        self.terminal_velocity = 10
        self.speed = 2

        self.position = pygame.math.Vector2(start_x, start_y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, self.gravity)

        self.arc = pygame.sprite.Group()
        self.poof = pygame.sprite.Group()

    def draw(self, display):
        self.arc.draw(display)
        self.poof.draw(display)
        display.blit(self.image, (self.rect.x + self.image_offset.x, self.rect.y + self.image_offset.x))

    def update(self, dt, tiles, spikes, border, camera, inventory_showing, enemies):
        self.border = border
        self.arc.update(self, enemies)
        if not inventory_showing:
            self.horizontal_movement(dt, camera)
            self.check_collisions_x(tiles, spikes)
            self.vertical_movement(dt)
            self.check_collisions_y(tiles, spikes)

    def horizontal_movement(self, dt, camera):
        self.acceleration.x = 0
        if self.LEFT_KEY:
            self.acceleration.x -= self.speed
        elif self.RIGHT_KEY:
            self.acceleration.x += self.speed
        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * dt
        self.limit_velocity(self.max_velocity)
        self.position.x += self.velocity.x * dt + (self.acceleration.x * 0.5) * (dt * dt)
        self.rect.x = self.position.x - camera.offset_float

    def vertical_movement(self, dt):
        self.velocity.y += self.acceleration.y * dt
        if self.velocity.y > self.terminal_velocity:
            self.velocity.y = self.terminal_velocity

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

    def get_collisions(self, tiles, spikes):
        hits = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hits.append(tile)
        return hits

    def check_collisions_x(self, tiles, spikes):
        collisions = self.get_collisions(tiles, spikes)
        for tile in collisions:
            if self.velocity.x > 0:
                temp_rect = self.rect.x
                self.rect.x = tile.left - self.rect.w
                adjust_factor = self.rect.x - temp_rect
                self.position.x += adjust_factor
                self.position.x = int(self.position.x)

            elif self.velocity.x < 0:
                temp_rect = self.rect.x
                self.rect.x = tile.right
                adjust_factor = self.rect.x - temp_rect
                self.position.x += adjust_factor
                self.position.x = int(self.position.x) + 1

    def check_collisions_y(self, tiles, spikes):
        self.on_ground = False
        self.rect.bottom += 1
        collisions = self.get_collisions(tiles, spikes)
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

    def update_frame(self, state):
        if not self.on_ground:
            if abs(self.velocity.x) > 0:
                if self.FACING_LEFT:
                    self.image = self.run_jump_left_frames
                else:
                    self.image = self.run_jump_right_frames
            else:
                if self.FACING_LEFT:
                    self.image = self.idle_jump_left_frames
                else:
                    self.image = self.idle_jump_right_frames
                    
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

    def turn(self, turning_left):
        state = "idle_right"
        if turning_left == self.FACING_LEFT:
            return
        elif not turning_left:
            state = "run_right"
        elif turning_left:
            state = "run_left"

        self.update_frame(state)

    def attack(self):
        if not self.arc.sprites():
            self.arc.add(Arc(['misc_assets/slash_fx/tile099.png',
                                        'misc_assets/slash_fx/tile100.png',
                                        'misc_assets/slash_fx/tile101.png',
                                        'misc_assets/slash_fx/tile102.png'], 40, (self.rect.x, self.rect.y), 1, self.FACING_LEFT))



class Arc(pygame.sprite.Sprite):
    def __init__(self, frames, interval, pos, scale, facingleft):
        pygame.sprite.Sprite.__init__(self)
        self.right_frames = []
        self.left_frames = []
        for frame in frames:
            self.right_frames.append(pygame.transform.scale(pygame.transform.scale_by(pygame.image.load(frame), scale), (96 * scale, 96 * scale + 20)))
            self.left_frames.append(pygame.transform.flip(pygame.transform.scale(pygame.transform.scale_by(pygame.image.load(frame), scale), (96 * scale, 96 * scale + 20)), 1, 0))

        self.interval = interval
        self.timer = 0
        self.timer_start = 0

        self.index = 0
        self.facingleft = facingleft

        self.pos = pos
        self.offset_right = pygame.math.Vector2(-10, -20)
        self.offset_left = pygame.math.Vector2(-45, -20)

        if self.facingleft:
            self.current_frames = self.left_frames
            self.offset = self.offset_left
        else:
            self.current_frames = self.right_frames
            self.offset = self.offset_right

        self.pos = (self.pos[0] + self.offset.x, self.pos[1] + self.offset.y)

        self.image = self.current_frames[self.index]
        self.rect = self.image.get_rect(topleft=self.pos)


    def update(self, player, enemies):
        self.timer = pygame.time.get_ticks()
        if self.timer_start == 0:
            self.timer_start = self.timer

        if self.timer - self.timer_start > self.interval:
            self.index += 1
            self.timer_start = self.timer
            if self.index >= len(self.current_frames):
                self.kill()
                self.index = 0

        self.image = self.current_frames[self.index]
        self.rect.x = player.rect.x + self.offset.x
        self.rect.y = player.rect.y + self.offset.y

        kills = self.check_kill(enemies)
        for kill in kills:
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
            ], (kill.rect.centerx, kill.rect.centery), 1, True))


    def check_kill(self, enemies):
        hits = []
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                hits.append(enemy)

        return hits















