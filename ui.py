import math
import pygame
from settings import *


class Inventory:
    def __init__(self, pos, offset, scale):
        self.image = pygame.transform.scale_by(pygame.image.load('ui/frame.png'), scale)
        self.offset = offset
        self.pos = pos
        self.panel1 = self.image.get_rect(center=(self.pos[0] - self.offset, self.pos[1]))
        self.panel2 = self.image.get_rect(center=(self.pos[0], self.pos[1]))
        self.panel3 = self.image.get_rect(center=(self.pos[0] + self.offset, self.pos[1]))

        self.showing = False

    def draw(self, display):
        if self.showing:
            display.blit(self.image, self.panel1)
            display.blit(self.image, self.panel2)
            display.blit(self.image, self.panel3)


class ItemSlot(pygame.sprite.Sprite):
    def __init__(self, inventory, slot_num, scale):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale_by(pygame.image.load('ui/itemslot1.png'), scale)
        self.x_offset = inventory.offset
        self.y_offset = 10
        self.spacing = 10
        self.line_height = 30
        self.slots_per_row = 4
        self.pos_x = self.x_offset - (inventory.panel3.w / 2) + (slot_num - (math.floor(slot_num / self.slots_per_row) * self.slots_per_row) * self.spacing)
        self.pos_y = ((HEIGHT / 2) - (inventory.panel3.h / 2) + self.y_offset) + (math.floor(slot_num / self.slots_per_row) * self.line_height)

        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))



















