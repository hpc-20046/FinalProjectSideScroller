# imports
import pygame
from settings import *
import random

# handles the spirit that drops from enemies
class SpiritFlame(pygame.sprite.Sprite):
    def __init__(self, pos, scale, spirit_range):
        pygame.sprite.Sprite.__init__(self)

        # frames for the spirit flame
        self.images = [
            pygame.transform.scale_by(pygame.image.load('misc_assets/spirit_flame/spr_blue_flame_0.png'), scale),
            pygame.transform.scale_by(pygame.image.load('misc_assets/spirit_flame/spr_blue_flame_1.png'), scale),
            pygame.transform.scale_by(pygame.image.load('misc_assets/spirit_flame/spr_blue_flame_2.png'), scale),
            pygame.transform.scale_by(pygame.image.load('misc_assets/spirit_flame/spr_blue_flame_3.png'), scale),
            pygame.transform.scale_by(pygame.image.load('misc_assets/spirit_flame/spr_blue_flame_4.png'), scale),
            pygame.transform.scale_by(pygame.image.load('misc_assets/spirit_flame/spr_blue_flame_5.png'), scale),
            pygame.transform.scale_by(pygame.image.load('misc_assets/spirit_flame/spr_blue_flame_6.png'), scale),
            pygame.transform.scale_by(pygame.image.load('misc_assets/spirit_flame/spr_blue_flame_7.png'), scale)
                       ]

        # images and rect
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pos
        # amount of spirit it is
        self.spirit_amount = random.randrange(spirit_range[0], spirit_range[1])

    # updates the frame for the flame
    def update_frame(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0

        self.image = self.images[self.index]

    # checks if it collides with the player
    def update(self, camera, player):
        if self.rect.colliderect(player.rect):
            player.spirit += self.spirit_amount
            self.kill()

        self.rect.x = self.pos[0] - camera.offset_float
        self.rect.y = self.pos[1]
