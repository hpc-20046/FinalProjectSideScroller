import math
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

        self.inventory = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.equip = [0, 0, 0, 0, 3]
        self.moving_slot = -1
        self.moving_equip_slot = -1

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
            case 4:
                self.icon.add(Icon(inventory, (self.icon_x, self.icon_y), pygame.image.load('ui/icons/items/tile115.png'), 2))
            case 5:
                self.icon.add(Icon(inventory, (self.icon_x, self.icon_y), pygame.image.load('ui/icons/items/tile119.png'), 2))
            case 6:
                self.icon.add(Icon(inventory, (self.icon_x, self.icon_y), pygame.image.load('ui/icons/items/tile131.png'), 2))

        self.icon.draw(screen)

    def drag(self, inventory):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and inventory.moving_slot != self.slot_num:
            inventory.moving_slot = self.slot_num

    def drop(self, inventory: Inventory):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if inventory.moving_slot == self.slot_num:
                inventory.moving_slot = -1
            elif inventory.moving_slot == -1 and inventory.moving_equip_slot == -1:
                return
            else:
                if inventory.inventory[self.slot_num] != 0:
                    inventory.moving_slot = -1
                    inventory.moving_equip_slot = -1
                else:
                    if inventory.moving_slot != -1:
                        inventory.inventory[self.slot_num] = inventory.inventory[inventory.moving_slot]
                        inventory.inventory[inventory.moving_slot] = 0
                        inventory.moving_slot = -1
                    elif inventory.moving_equip_slot != -1:
                        inventory.inventory[self.slot_num] = inventory.equip[inventory.moving_equip_slot - 1]
                        inventory.equip[inventory.moving_equip_slot - 1] = 0
                        inventory.moving_equip_slot = -1




class EquipSlot(pygame.sprite.Sprite):
    def __init__(self, inventory, slot_num, scale):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.transform.scale_by(pygame.image.load('ui/equipslot.png'), scale)
        self.pos = pygame.math.Vector2(0,0)
        self.slot_num = slot_num

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
                
        self.icon_x = self.pos.x
        self.icon_y = self.pos.y
        
        self.icon = pygame.sprite.Group()
                
        self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y))
        
    def update(self, inventory, screen):
        self.icon.empty()
        
        if inventory.moving_equip_slot == self.slot_num:
            self.icon_x = pygame.mouse.get_pos()[0]
            self.icon_y = pygame.mouse.get_pos()[1]
        else:
            self.icon_x = self.pos.x
            self.icon_y = self.pos.y

        match inventory.equip[self.slot_num - 1]:
            case 0:
                self.icon.add(Icon(inventory, (self.icon_x, self.icon_y), pygame.image.load('ui/icons/blank.png'), 1))
            case 1:
                self.icon.add(Icon(inventory, (self.icon_x, self.icon_y), pygame.image.load('ui/icons/items/tile082.png'), 2))
            case 2:
                self.icon.add(Icon(inventory, (self.icon_x, self.icon_y), pygame.image.load('ui/icons/items/tile081.png'), 2))
            case 3:
                self.icon.add(Icon(inventory, (self.icon_x, self.icon_y), pygame.image.load('ui/icons/items/tile080.png'), 2))
            case 4:
                self.icon.add(Icon(inventory, (self.icon_x, self.icon_y), pygame.image.load('ui/icons/items/tile115.png'), 2))
            case 5:
                self.icon.add(Icon(inventory, (self.icon_x, self.icon_y), pygame.image.load('ui/icons/items/tile119.png'), 2))
            case 6:
                self.icon.add(Icon(inventory, (self.icon_x, self.icon_y), pygame.image.load('ui/icons/items/tile131.png'), 2))

        self.icon.draw(screen)

    def drag(self, inventory):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and inventory.moving_equip_slot != self.slot_num:
            inventory.moving_equip_slot = self.slot_num

    def drop(self, inventory: Inventory):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if inventory.moving_equip_slot == self.slot_num:
                inventory.moving_equip_slot = -1
            elif inventory.moving_slot == -1 and inventory.moving_equip_slot == -1:
                return
            else:
                if inventory.equip[self.slot_num - 1] != 0:
                    inventory.moving_slot = -1
                    inventory.moving_equip_slot = -1
                else:
                    if inventory.moving_slot != -1:
                        inventory.equip[self.slot_num - 1] = inventory.inventory[inventory.moving_slot]
                        inventory.inventory[inventory.moving_slot] = 0
                        inventory.moving_slot = -1
                    elif inventory.moving_equip_slot != -1:
                        inventory.equip[self.slot_num - 1] = inventory.equip[inventory.moving_equip_slot - 1]
                        inventory.equip[inventory.moving_equip_slot - 1] = 0
                        inventory.moving_equip_slot = -1


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
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)


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
    def __init__(self, pos, scale, attr_num):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale_by(pygame.image.load('ui/add.png'), scale)
        self.rect = self.image.get_rect(center=pos)
        self.attr_num = attr_num

    def click(self, player):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            player.attributes[self.attr_num] += 1
            if player.attributes[self.attr_num] > 10:
                player.attributes[self.attr_num] -= 1
                return
            if player.spirit < 5:
                player.attributes[self.attr_num] -= 1
            else:
                player.spirit -= 5


class UiText(pygame.sprite.Sprite):
    def __init__(self, text, font, size, colour, pos):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(font, size)
        self.image = self.font.render(text, True, colour)
        self.rect = self.image.get_rect(topleft=pos)
        

class AnimatedImage(pygame.sprite.Sprite):
    def __init__(self, images, pos, scale, playonce, usingcamera, camera, use_center):
        pygame.sprite.Sprite.__init__(self)
        
        self.images = []
        self.using_camera = usingcamera
        
        for i in range(len(images)):
            self.images.append(pygame.transform.scale_by(pygame.image.load(images[i]), scale))

        self.pos = pos
        self.use_center = use_center
        self.index = 0

        self.image = self.images[self.index]
        if use_center:
            if self.using_camera:
                self.rect = self.image.get_rect(center=(pos[0] - camera.offset_float, pos[1]))
            else:
                self.rect = self.image.get_rect(center=pos)
        else:
            if self.using_camera:
                self.rect = self.image.get_rect(topleft=(pos[0] - camera.offset_float, pos[1]))
            else:
                self.rect = self.image.get_rect(topleft=pos)
        self.playonce = playonce
        
    def update(self, camera):
        self.index += 1
        if self.index > len(self.images) - 1:
            if self.playonce:
                self.kill()
                self.index = 0
            else:
                self.index = 0
        
        self.image = self.images[self.index]
        if self.using_camera:
            if self.use_center:
                self.rect.centerx = self.pos[0] - camera.offset_float
                self.rect.centery = self.pos[1]
            else:
                self.rect.x = self.pos[0] - camera.offset_float
                self.rect.y = self.pos[1]



class SpiritAmount(pygame.sprite.Sprite):
    def __init__(self, text, font, size, colour, positions):
        pygame.sprite.Sprite.__init__(self)
        
        self.colour = colour
        self.font = pygame.font.Font(font, size)
        self.image = self.font.render(str(text), True, colour)
        self.positions = positions
        self.index = 0
        self.rect = self.image.get_rect(center=positions[self.index])

        self.offset = 7
        
    def update(self, amount):
        self.image = self.font.render(str(amount), True, self.colour)
        offset = 0
        if amount > 9:
            offset = self.offset
        if amount > 99:
            offset = self.offset * 2
        if amount > 999:
            offset = self.offset * 3

        self.index += 1
        if self.index >= len(self.positions):
            self.index = 0
        self.rect.centerx = self.positions[self.index][0] - offset
        self.rect.centery = self.positions[self.index][1]


class TutorialText(pygame.sprite.Sprite):
    def __init__(self, text, font, size, colour, pos, level):
        pygame.sprite.Sprite.__init__(self)

        self.colour = colour
        self.text = text
        self.font = pygame.font.Font(font, size)
        self.image = self.font.render(text, True, self.colour)
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pos
        self.level = level

    def update(self, camera, current_level):
        if not current_level == self.level:
            self.image = self.font.render(' ', True, self.colour)
        else:
            self.image = self.font.render(self.text, True, self.colour)
            self.rect.x = self.pos[0] - camera.offset_float


class AnimatedLevelImage(pygame.sprite.Sprite):
    def __init__(self, images, pos, scale, level, attackable, health):
        pygame.sprite.Sprite.__init__(self)

        self.images = []
        for image in images:
            self.images.append(pygame.transform.scale_by(pygame.image.load(image), scale))

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=pos)
        self.pos = pos
        self.level = level
        self.showing = False
        self.attackable = attackable
        self.shaking = True
        self.timex = 8
        self.timey = 0
        self.x = 0
        self.y = 0
        self.damagable = True
        self.health = health


    def update(self, current_level, player):
        if self.level == current_level:
            self.showing = True
            self.image = self.images[self.index]
        else:
            self.showing = False
            self.image = pygame.image.load('ui/icons/blank.png')

        if player.arc.sprites():
            if self.rect.colliderect(player.arc.sprites()[0]):
                if self.attackable:
                    self.timex = 0
                    self.attackable = False
                    self.health -= 1

        if self.timex > 4:
            self.attackable = True

        if self.health <= 0:
            self.delete()

        self.shake()
        self.timex += 0.1
        self.timey += 0.05

        self.y = math.sin(self.timey) * 5
        self.rect.centery = self.pos[1] + self.y

    def update_frame(self):
        self.index += 1

        if self.index >= len(self.images):
            self.index = 0

        if self.showing:
            self.image = self.images[self.index]
        else:
            self.image = pygame.image.load('ui/icons/blank.png')

    def delete(self):
        self.kill()
        self.image = pygame.image.load('ui/icons/blank.png')
        self.showing = False

    def shake(self):
        if self.shaking:
            self.x = math.exp(-self.timex) * math.cos(15 * self.timex) * 15
            self.rect.centerx = self.pos[0] + self.x


class HealthBar:
    def __init__(self, scale, pos):
        self.empty = pygame.transform.scale_by(pygame.image.load('ui/MinimalFantasy/ValueBar_128x16.png'), scale)
        self.bar = pygame.transform.scale_by(pygame.image.load('ui/MinimalFantasy/ValueRed_120x8.png'), scale)
        self.offset = pygame.math.Vector2(4, 4)

        self.rect = self.empty.get_rect(topleft=pos)
        self.bar_rect = self.bar.get_rect(topleft=(pos[0] + self.offset.x * scale, pos[1] + self.offset.y * scale))

        self.amount = 100
        self.total = 100
        self.start_total = 100
        
        self.time = 0
        self.iframe_start = 0
        self.iframe_length = 500
        
        self.damageable = True
        
    def update(self, player):
        self.time = pygame.time.get_ticks()

        self.total = self.start_total + player.attributes[0] * 10

        
        if self.time - self.iframe_start >= self.iframe_length:
            self.damageable = True

    def draw(self, display):
        bar_width = self.bar_rect.w * (self.amount / self.total)

        display.blit(self.empty, self.rect)
        display.blit(self.bar, self.bar_rect, area=(0, 0, bar_width, self.bar_rect.h))

    def damage(self, damage, player):
        if self.damageable:
            damage = damage - player.attributes[2]
            if damage < 0:
                damage = 0
            self.amount -= damage
            if self.amount < 0:
                self.amount = 0
            self.iframe_start = self.time
            self.damageable = False
            player.hit = True


class Item(pygame.sprite.Sprite):
    def __init__(self, pos, item_num, scale):
        pygame.sprite.Sprite.__init__(self)

        match item_num:
            case 1:
                self.image = pygame.transform.scale_by(pygame.image.load('ui/icons/items/tile082.png'), scale)
            case 2:
                self.image = pygame.transform.scale_by(pygame.image.load('ui/icons/items/tile081.png'), scale)
            case 3:
                self.image = pygame.transform.scale_by(pygame.image.load('ui/icons/items/tile080.png'), scale)
            case 4:
                self.image = pygame.transform.scale_by(pygame.image.load('ui/icons/items/tile115.png'), scale)
            case 5:
                self.image = pygame.transform.scale_by(pygame.image.load('ui/icons/items/tile119.png'), scale)
            case 6:
                self.image = pygame.transform.scale_by(pygame.image.load('ui/icons/items/tile131.png'), scale)

        self.rect = self.image.get_rect(center=pos)
        self.pos = pos
        self.x = 0
        self.y = 0
        self.item_num = item_num

    def update(self, player, camera, inventory):
        self.x += 0.05
        self.y = math.sin(self.x) * 10
        self.rect.y = self.pos[1] + self.y
        self.rect.x = self.pos[0] - camera.offset_float

        if self.rect.colliderect(player.rect):
            try:
                inventory.inventory[inventory.inventory.index(0)] = self.item_num
                self.kill()
            except ValueError:
                return
