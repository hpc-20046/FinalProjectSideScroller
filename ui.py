import math
from tkinter import SEL
import pygame
from settings import *


class Inventory:
    def __init__(self, pos, offset, scale):
        self.image = pygame.transform.scale_by(pygame.image.load('ui/frame.png'), scale)
        self.middle_image = pygame.transform.scale_by(pygame.image.load('ui/centre_frame.png'), scale)
        self.offset = offset
        self.pos = pos
        self.panel1 = self.image.get_rect(center=(self.pos[0] - self.offset, self.pos[1]))
        self.panel2 = self.image.get_rect(center=(self.pos[0], self.pos[1]))
        self.panel3 = self.image.get_rect(center=(self.pos[0] + self.offset, self.pos[1]))

        self.showing = False

        self.inventory = [1, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.moving_slot = -1

    def draw(self, display):
        if self.showing:
            display.blit(self.image, self.panel1)
            display.blit(self.middle_image, self.panel2)
            display.blit(self.image, self.panel3)

    def update(self):
        pass


class InventorySlot(pygame.sprite.Sprite):
    def __init__(self, inventory, slot_num, scale):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale_by(pygame.image.load('ui/itemslot1.png'), scale)
        self.inventory_offset = inventory.offset
        self.x_offset = 120
        self.y_offset = 110
        self.spacing = 90
        self.line_height = 90
        self.slots_per_row = 4
        self.slot_num = slot_num
        self.pos_x = (WIDTH / 2) + self.inventory_offset - (inventory.panel3.w / 2) + self.x_offset + (slot_num - ((math.floor(slot_num / self.slots_per_row)) * self.slots_per_row)) * self.spacing
        self.pos_y = ((HEIGHT / 2) - (inventory.panel3.h / 2) + self.y_offset) + (math.floor(slot_num / self.slots_per_row) * self.line_height)

        self.icon_x = self.pos_x
        self.icon_y = self.pos_y

        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))
        self.icon = pygame.sprite.Group()

        self.icon.add(Icon(inventory, (self.pos_x, self.pos_y), pygame.image.load('ui/icons/blank.png'), 1))

    def update(self, inventory, screen):
        self.icon.empty()

        if inventory.moving_slot == self.slot_num:
            self.icon_x = pygame.mouse.get_pos()[0]
            self.icon_y = pygame.mouse.get_pos()[1]
        else:
            self.icon_x, self.icon_y = self.pos_x, self.pos_y


        match inventory.inventory[self.slot_num]:
            case 0:
                self.icon.add(Icon(inventory, (self.icon_x, self.icon_y), pygame.image.load('ui/icons/blank.png'), 1))
            case 1:
                self.icon.add(Icon(inventory, (self.icon_x, self.icon_y), pygame.image.load('ui/icons/items/tile082.png'), 2))
            case 2:
                self.icon.add(Icon(inventory, (self.icon_x, self.icon_y), pygame.image.load('ui/icons/items/tile081.png'), 2))
            case 3:
                self.icon.add(Icon(inventory, (self.icon_x, self.icon_y), pygame.image.load('ui/icons/items/tile080.png'), 2))

        self.icon.draw(screen)

    def drag(self, inventory):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and inventory.moving_slot != self.slot_num:
            inventory.moving_slot = self.slot_num

    def drop(self, inventory):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if inventory.moving_slot == self.slot_num:
                inventory.moving_slot = -1
            else:
                if inventory.inventory[self.slot_num] != 0:
                    inventory.moving_slot = -1
                else:
                    inventory.inventory[self.slot_num] = inventory.inventory[inventory.moving_slot]
                    inventory.inventory[inventory.moving_slot] = 0
                    inventory.moving_slot = -1




class EquipSlot(pygame.sprite.Sprite):
    def __init__(self, inventory, slot_num, scale):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.transform.scale_by(pygame.image.load('ui/equipslot.png'), scale)
        self.pos = pygame.math.Vector2(0,0)

        match slot_num:
            case 1:
                self.pos.x = (WIDTH / 2) - 150
                self.pos.y = (HEIGHT / 2) + 220
            case 2:
                self.pos.x = (WIDTH / 2) - 50
                self.pos.y = (HEIGHT / 2) + 220
            case 3:
                self.pos.x = (WIDTH / 2) + 50
                self.pos.y = (HEIGHT / 2) + 220
            case 4:
                self.pos.x = (WIDTH / 2) + 150
                self.pos.y = (HEIGHT / 2) + 220
            case 5:
                self.pos.x = (WIDTH / 2)
                self.pos.y = (HEIGHT / 2) + 120
            case _:
                self.pos.x = 0
                self.pos.y = 0
                
        self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y))

    def drag(self, inventory):
        pass

    def drop(self, inventory):
        pass


class PlayerBorder(pygame.sprite.Sprite):
    def __init__(self, inventory, scale):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale_by(pygame.image.load('ui/player_border.png'), scale)
        self.pos = inventory.pos
        self.y_offset = -100
        self.rect = self.image.get_rect(center=(self.pos[0], self.pos[1] + self.y_offset))


class Icon(pygame.sprite.Sprite):
    def __init__(self, inventory, pos, image, scale):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale_by(image, scale)
        self.rect = self.image.get_rect(center=(pos[0], pos[1]))


class AttributeBar:
    def __init__(self, inventory, pos, scale):
        self.image = pygame.transform.scale_by(pygame.image.load('ui/attributeBarEmpty.png'), scale)
        self.fill_image = pygame.transform.scale_by(pygame.image.load('ui/attributeBarActive.png'), scale)
        self.rect = self.image.get_rect(topleft=pos)
        self.fill_image_rect = self.fill_image.get_rect()
    
    def draw(self, display, amount):
        display.blit(self.image, self.rect)
        for i in range(amount):
            display.blit(self.fill_image, (self.rect.x + (i * self.fill_image_rect.w), self.rect.y))
            
class AttributeButton(pygame.sprite.Sprite):
    def __init__(self, pos, scale):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale_by(pygame.image.load('ui/add.png'), scale)
        self.rect = self.image.get_rect(center=pos)


class UiText(pygame.sprite.Sprite):
    def __init__(self, text, font, size, colour, pos):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(font, size)
        self.image = self.font.render(text, True, colour)
        self.rect = self.image.get_rect(topleft=pos)
        

class AnimatedImage(pygame.sprite.Sprite):
    def __init__(self, images, pos, scale):
        pygame.sprite.Sprite.__init__(self)
        
        self.images = []
        
        for i in range(len(images)):
            self.images.append(pygame.transform.scale_by(pygame.image.load(images[i]), scale))

        self.image = self.images[0]
        self.rect = self.image.get_rect(center=pos)
        self.index = 0
        
    def update(self):
        self.index += 1
        if self.index > len(self.images) - 1:
            self.index = 0
        
        self.image = self.images[self.index]

