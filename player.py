import random
import pygame
from settings import *
from spirit import SpiritFlame
from ui import AnimatedImage, Item


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


        self.state_frames = self.idle_right_frames
        self.frame_index = 0
        self.image = self.idle_right_frames[self.frame_index]
        self.image_offset = pygame.math.Vector2(-9 * scale_factor, -9 * scale_factor)
        self.border = border

        self.rect = pygame.Rect(start_x, start_y, 13 * scale_factor, 19 * scale_factor)

        self.state = "idle_right"
        self.temp_state = ""

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
        self.flame = pygame.sprite.Group()
        self.item = pygame.sprite.Group()

        self.damage = 5
        self.spirit = 0

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
        self.temp_facing = False


    def draw(self, display):
        self.arc.draw(display)
        self.flame.draw(display)
        self.item.draw(display)
        self.poof.draw(display)
        display.blit(self.image, (self.rect.x + self.image_offset.x, self.rect.y + self.image_offset.x))

    def update(self, dt, tiles, spikes, border, camera, inventory, enemies, bar, current_level):
        self.time = pygame.time.get_ticks()
        if self.time - self.time_start >= 400:
            self.max_velocity = 4
            self.dash = False
            self.dashing = False

        self.border = border
        self.arc.update(self, enemies, camera)
        self.flame.update(camera, self)
        self.item.update(self, camera, inventory)
        if not inventory.showing:
            self.horizontal_movement(dt, camera)
            self.check_collisions_x(tiles, spikes)
            if not self.dash:
                self.vertical_movement(dt)
                self.check_collisions_y(tiles, spikes)

        if self.time - self.death_time_start >= 3000 and self.death_anim:
            self.dead = False
            self.death_anim = False
            self.hit = False
            self.hurt = False
            self.respawn(current_level, camera, bar)

        if bar.amount <= 0:
            self.dead = True

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
        impaled = False
        for tile in tiles:
            if self.rect.colliderect(tile):
                hits.append(tile)

        for spike in spikes:
            if self.rect.colliderect(spike):
                impaled = True
                break
        return hits, impaled

    def check_collisions_x(self, tiles, spikes):
        collisions, spike = self.get_collisions(tiles, spikes)
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
        if spike:
            self.dead = True

    def check_collisions_y(self, tiles, spikes):
        self.on_ground = False
        self.rect.bottom += 1
        collisions, spike = self.get_collisions(tiles, spikes)
        if spike:
            self.dead = True
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


    def roll(self):
        if not self.time - self.time_start >= self.cooldown:
            return

        if self.FACING_LEFT:
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
        self.update_frame("roll", True, False, "")


    def update_frame(self, state, roll, hit, player_state):
        if self.dead:
            self.temp_state = state
            if not self.death_anim:
                if self.FACING_LEFT:
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
                self.death_time_start = self.time
            else:
                if not roll and not hit:
                    if self.alternate:
                        self.frame_index += 1
                        if self.frame_index >= len(self.state_frames):
                            self.frame_index -= 1
                        self.image = self.state_frames[self.frame_index]

                    self.alternate = not self.alternate

        else:
            if self.dash:
                self.temp_state = state
                if not self.dashing:
                    if self.FACING_LEFT:
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
                    if roll:
                        self.frame_index += 1
                        if self.frame_index >= len(self.state_frames):
                            self.frame_index -= 1
                        self.image = self.state_frames[self.frame_index]

            elif self.hit:
                self.temp_state = state
                if not self.hurt:
                    if self.FACING_LEFT:
                        self.state_frames = self.hit_left_frames
                        self.frame_index = 0
                        self.image = self.state_frames[self.frame_index]
                        self.hurt = True
                    else:
                        self.state_frames = self.hit_right_frames
                        self.frame_index = 0
                        self.image = self.state_frames[self.frame_index]
                        self.hurt = True
                    self.temp_facing = self.FACING_LEFT
                else:
                    if hit:
                        if self.temp_facing != self.FACING_LEFT:
                            if self.FACING_LEFT:
                                self.state_frames = self.hit_left_frames
                            else:
                                self.state_frames = self.hit_right_frames
                            self.temp_facing = self.FACING_LEFT

                        self.frame_index += 1
                        if self.frame_index >= len(self.state_frames):
                            self.frame_index -= 1
                            self.hit = False
                            self.hurt = False
                        self.image = self.state_frames[self.frame_index]

            else:
                if not roll and not hit:
                    if not self.temp_state == "":

                        player_state = ""

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

                        self.temp_state = ""

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




        return player_state

    def respawn(self, current_level, camera, bar):
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

        if bar.amount > 0:
            bar.damage(10, self)
        else:
            bar.amount = 100


    def turn(self, turning_left, player_state):
        state = "idle_right"
        if turning_left == self.FACING_LEFT:
            return
        elif not turning_left:
            state = "run_right"
        elif turning_left:
            state = "run_left"

        player_state = self.update_frame(state, False, False, player_state)

        return player_state

    def attack(self, camera):
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

        self.damaged = False


    def update(self, player, enemies, camera):
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
            if not self.damaged:
                kill.health -= player.damage
                self.damaged = True
                kill.knockback(player.FACING_LEFT)

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

                if kill.type == 2:
                    player.item.add(Item((kill.position.x, kill.position.y - kill.rect.h), 1, 1.5))
                else:
                    player.flame.add(SpiritFlame((kill.position.x, kill.position.y - kill.rect.h - 20), 3, (1, 3)))
                    if random.random() <= 0.2:
                        player.item.add(Item((kill.position.x, kill.position.y - kill.rect.h), random.randrange(1, 6), 1.5))

    def check_kill(self, enemies):
        hits = []
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                hits.append(enemy)

        return hits

