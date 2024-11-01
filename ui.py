import math
import random
import pygame
from settings import *

# class that handles everything in the inventory
class Inventory:
    def __init__(self, pos, offset, scale):
        # images, positions, and rects
        self.image = pygame.transform.scale_by(pygame.image.load('ui/frame.png'), scale)
        self.middle_image = pygame.transform.scale_by(pygame.image.load('ui/centre_frame.png'), scale)
        self.offset = offset
        self.pos = pos
        self.panel1 = self.image.get_rect(center=(self.pos[0] - self.offset, self.pos[1]))
        self.panel2 = self.image.get_rect(center=(self.pos[0], self.pos[1]))
        self.panel3 = self.image.get_rect(center=(self.pos[0] + self.offset, self.pos[1]))

        # start with inventory not showing
        self.showing = False

        # list of everything that's in the bag or equipped
        self.inventory = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.equip = [0, 0, 0, 0, 0]
        # stores what slot is currently being moved
        self.moving_slot = -1
        self.moving_equip_slot = -1

    # draws the inventory panels
    def draw(self, display):
        if self.showing:
            display.blit(self.image, self.panel1)
            display.blit(self.middle_image, self.panel2)
            display.blit(self.image, self.panel3)

# object for a single slot in the item bag
class InventorySlot(pygame.sprite.Sprite):
    def __init__(self, inventory, slot_num, scale):
        pygame.sprite.Sprite.__init__(self)

        # images
        self.image = pygame.transform.scale_by(pygame.image.load('ui/itemslot1.png'), scale)

        # position variables
        self.inventory_offset = inventory.offset
        self.x_offset = 120
        self.y_offset = 110
        self.spacing = 90
        self.line_height = 90
        self.slots_per_row = 4
        self.slot_num = slot_num
        self.pos_x = ((WIDTH / 2) + self.inventory_offset - (inventory.panel3.w / 2) + self.x_offset
                      + (slot_num - ((math.floor(slot_num / self.slots_per_row)) * self.slots_per_row)) * self.spacing)
        self.pos_y = ((HEIGHT / 2) - (inventory.panel3.h / 2) + self.y_offset) + (math.floor(slot_num / self.slots_per_row) * self.line_height)
        self.icon_x = self.pos_x
        self.icon_y = self.pos_y

        # rect
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))
        # icon group
        self.icon = pygame.sprite.Group()

        # start with the slot empty
        self.icon.add(Icon(inventory, (self.pos_x, self.pos_y), pygame.image.load('ui/icons/blank.png'), 1))

    # update the slot
    def update(self, inventory, screen):
        # make sure only drawing one item
        self.icon.empty()

        # if this slot is being moved, make the icon follow the mouse
        if inventory.moving_slot == self.slot_num:
            self.icon_x = pygame.mouse.get_pos()[0]
            self.icon_y = pygame.mouse.get_pos()[1]
        else:
            self.icon_x, self.icon_y = self.pos_x, self.pos_y

        # draw the item that is currently stored in the slot
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
            case 7:
                self.icon.add(Icon(inventory, (self.icon_x, self.icon_y), pygame.image.load('ui/icons/items/tile122.png'), 2))

        # draw the icons
        self.icon.draw(screen)

    # runs when MOUSEBUTTONDOWN
    def drag(self, inventory):
        # if the mouse clicks on the slot, set it to the moving slot
        if self.rect.collidepoint(pygame.mouse.get_pos()) and inventory.moving_slot != self.slot_num:
            inventory.moving_slot = self.slot_num

    # runs when MOUSEBUTTONUP
    def drop(self, inventory: Inventory):
        # if the mouse drops an item on this slot
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            # reset if it drops it on itself
            if inventory.moving_slot == self.slot_num:
                inventory.moving_slot = -1
            # cancel if nothing is attached to the mouse
            elif inventory.moving_slot == -1 and inventory.moving_equip_slot == -1:
                return
            else:
                # reset if this slot already has something in it
                if inventory.inventory[self.slot_num] != 0:
                    inventory.moving_slot = -1
                    inventory.moving_equip_slot = -1
                else:
                    # set the item attached to the mouse to the item in this slot and delete it
                    if inventory.moving_slot != -1:
                        inventory.inventory[self.slot_num] = inventory.inventory[inventory.moving_slot]
                        inventory.inventory[inventory.moving_slot] = 0
                        inventory.moving_slot = -1
                    # same, but if coming from an equip slot
                    elif inventory.moving_equip_slot != -1:
                        inventory.inventory[self.slot_num] = inventory.equip[inventory.moving_equip_slot - 1]
                        inventory.equip[inventory.moving_equip_slot - 1] = 0
                        inventory.moving_equip_slot = -1

# item slot of the equip variant
class EquipSlot(pygame.sprite.Sprite):
    def __init__(self, inventory, slot_num, scale):
        pygame.sprite.Sprite.__init__(self)

        # images and other variables
        self.image = pygame.transform.scale_by(pygame.image.load('ui/equipslot.png'), scale)
        self.pos = pygame.math.Vector2(0,0)
        self.slot_num = slot_num

        # position based on slot number
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
        # rect
        self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y))

    # updates the slot
    def update(self, inventory, screen):
        self.icon.empty()

        # attaches the item to the mouse if this slot is moving
        if inventory.moving_equip_slot == self.slot_num:
            self.icon_x = pygame.mouse.get_pos()[0]
            self.icon_y = pygame.mouse.get_pos()[1]
        else:
            self.icon_x = self.pos.x
            self.icon_y = self.pos.y

        # draw the item
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
            case 7:
                self.icon.add(Icon(inventory, (self.icon_x, self.icon_y), pygame.image.load('ui/icons/items/tile122.png'), 2))

        self.icon.draw(screen)

    def drag(self, inventory):
        # if the mouse clicks on this slot, attach the item to the mouse
        if self.rect.collidepoint(pygame.mouse.get_pos()) and inventory.moving_equip_slot != self.slot_num:
            inventory.moving_equip_slot = self.slot_num

    def drop(self, inventory: Inventory):
        # if the mouse drops on this slot
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            # reset if it's dropped on the same slot
            if inventory.moving_equip_slot == self.slot_num:
                inventory.moving_equip_slot = -1
            # cancel if nothing is moving
            elif inventory.moving_slot == -1 and inventory.moving_equip_slot == -1:
                return
            else:
                # reset if there's already something in the slot
                if inventory.equip[self.slot_num - 1] != 0:
                    inventory.moving_slot = -1
                    inventory.moving_equip_slot = -1
                else:
                    # set the moving item to this slot and delete it from the other
                    if inventory.moving_slot != -1:
                        inventory.equip[self.slot_num - 1] = inventory.inventory[inventory.moving_slot]
                        inventory.inventory[inventory.moving_slot] = 0
                        inventory.moving_slot = -1
                    elif inventory.moving_equip_slot != -1:
                        inventory.equip[self.slot_num - 1] = inventory.equip[inventory.moving_equip_slot - 1]
                        inventory.equip[inventory.moving_equip_slot - 1] = 0
                        inventory.moving_equip_slot = -1

# for the outline of the player in the inventory
class PlayerBorder(pygame.sprite.Sprite):
    def __init__(self, inventory, scale):
        pygame.sprite.Sprite.__init__(self)
        # image, pos and rect
        self.image = pygame.transform.scale_by(pygame.image.load('ui/player_border.png'), scale)
        self.pos = inventory.pos
        self.y_offset = -100
        self.rect = self.image.get_rect(center=(self.pos[0], self.pos[1] + self.y_offset))

# icon. used for inventory slots and other visuals
class Icon(pygame.sprite.Sprite):
    def __init__(self, inventory, pos, image, scale):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale_by(image, scale)
        self.rect = self.image.get_rect(center=(pos[0], pos[1]))
    # draws the icon
    def draw(self, screen):
        screen.blit(self.image, self.rect)

# attribute bars for the inventory
class AttributeBar:
    def __init__(self, inventory, pos, scale):
        # images and rects
        self.image = pygame.transform.scale_by(pygame.image.load('ui/attributeBarEmpty.png'), scale)
        self.fill_image = pygame.transform.scale_by(pygame.image.load('ui/attributeBarActive.png'), scale)
        self.rect = self.image.get_rect(topleft=pos)
        self.fill_image_rect = self.fill_image.get_rect()
    # draws the bar and all the fill indicators
    def draw(self, display, amount):
        display.blit(self.image, self.rect)
        for i in range(amount):
            display.blit(self.fill_image, (self.rect.x + (i * self.fill_image_rect.w), self.rect.y))

# the buttons for upgrading the player
class AttributeButton(pygame.sprite.Sprite):
    def __init__(self, pos, scale, attr_num):
        pygame.sprite.Sprite.__init__(self)
        # images
        self.image = pygame.transform.scale_by(pygame.image.load('ui/add.png'), scale)
        self.rect = self.image.get_rect(center=pos)
        # num and sound
        self.attr_num = attr_num
        self.click_sound = pygame.mixer.Sound('audio/click.wav')

    # upgrades the player when clicking on the button
    def click(self, player):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            player.attributes[self.attr_num] += 1
            # caps it to 10
            if player.attributes[self.attr_num] > 10:
                player.attributes[self.attr_num] -= 1
                return
            # doesn't upgrade if less than 5 spirit
            if player.spirit < 5:
                player.attributes[self.attr_num] -= 1
                return
            else:
                player.spirit -= 5
            self.click_sound.play()
            # restore the health if upgrading it
            if self.attr_num == 0:
                player.health_update = True

# text for the inventory
class UiText(pygame.sprite.Sprite):
    def __init__(self, text, font, size, colour, pos):
        pygame.sprite.Sprite.__init__(self)
        # image and rect
        self.font = pygame.font.Font(font, size)
        self.image = self.font.render(text, True, colour)
        self.rect = self.image.get_rect(topleft=pos)
        
# image that is animated
class AnimatedImage(pygame.sprite.Sprite):
    def __init__(self, images, pos, scale, playonce, usingcamera, camera, use_center):
        pygame.sprite.Sprite.__init__(self)

        # images
        self.images = []
        self.using_camera = usingcamera
        
        for i in range(len(images)):
            self.images.append(pygame.transform.scale_by(pygame.image.load(images[i]), scale))

        # positions
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
        # update the image
        self.index += 1
        # delete it if play only once
        if self.index > len(self.images) - 1:
            if self.playonce:
                self.kill()
                self.index = 0
            else:
                self.index = 0
        # update image and image
        self.image = self.images[self.index]
        if self.using_camera:
            if self.use_center:
                self.rect.centerx = self.pos[0] - camera.offset_float
                self.rect.centery = self.pos[1]
            else:
                self.rect.x = self.pos[0] - camera.offset_float
                self.rect.y = self.pos[1]


# displays the amount of spirit on the inventory
class SpiritAmount(pygame.sprite.Sprite):
    def __init__(self, text, font, size, colour, positions):
        pygame.sprite.Sprite.__init__(self)

        # image and rect
        self.colour = colour
        self.font = pygame.font.Font(font, size)
        self.image = self.font.render(str(text), True, colour)
        self.positions = positions
        self.index = 0
        self.rect = self.image.get_rect(center=positions[self.index])

        self.offset = 7

    def update(self, amount):
        # offsets to stay centered
        self.image = self.font.render(str(amount), True, self.colour)
        offset = 0
        if amount > 9:
            offset = self.offset
        if amount > 99:
            offset = self.offset * 2
        if amount > 999:
            offset = self.offset * 3

        # update image and position
        self.index += 1
        if self.index >= len(self.positions):
            self.index = 0
        self.rect.centerx = self.positions[self.index][0] - offset
        self.rect.centery = self.positions[self.index][1]

# text that goes on the wall for the tutorial
class TutorialText(pygame.sprite.Sprite):
    def __init__(self, text, font, size, colour, pos, level):
        pygame.sprite.Sprite.__init__(self)

        # images, rects, and other stuff
        self.colour = colour
        self.text = text
        self.font = pygame.font.Font(font, size)
        self.image = self.font.render(text, True, self.colour)
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pos
        self.level = level

    # updates the pos for the camera
    def update(self, camera, current_level):
        if not current_level == self.level:
            self.image = self.font.render(' ', True, self.colour)
        else:
            self.image = self.font.render(self.text, True, self.colour)
            self.rect.x = self.pos[0] - camera.offset_float

# animated image just for one level. used for the heart
class AnimatedLevelImage(pygame.sprite.Sprite):
    def __init__(self, images, pos, scale, level, attackable, health):
        pygame.sprite.Sprite.__init__(self)
         # images
        self.images = []
        for image in images:
            self.images.append(pygame.transform.scale_by(pygame.image.load(image), scale))

        # rect, pos, and event variables
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
        self.exploded = False
        self.health = health

        # sounds
        self.hurt_sound = pygame.mixer.Sound('audio/heart_hit.wav')
        self.hurt_sound.set_volume(0.3)
        self.kill_sound = pygame.mixer.Sound('audio/heart_kill.wav')


    def update(self, current_level, player):
        # show if on current level
        if self.level == current_level:
            self.showing = True
            self.image = self.images[self.index]
        else:
            self.showing = False
            self.image = pygame.image.load('ui/icons/blank.png')

        # detect if attacked
        if player.arc.sprites():
            if self.rect.colliderect(player.arc.sprites()[0]):
                # damage the image
                if self.attackable and not self.exploded and self.showing:
                    self.timex = 0
                    self.attackable = False
                    self.health -= 1
                    
                    if self.health != 0:
                        player.arc.sprites()[0].sound_played = True
                        self.hurt_sound.play()
                    
        # attack cooldown
        if self.timex > 4:
            self.attackable = True

        # explosion on death
        if self.health <= 0:
            player.explosion = True
            self.health = 100000
            self.exploded = True
            self.kill_sound.play()

        # shake for attack indicator
        self.shake()
        self.timex += 0.1
        self.timey += 0.05

        # bob based on sine wave
        self.y = math.sin(self.timey) * 5
        self.rect.centery = self.pos[1] + self.y

    # updates the image
    def update_frame(self):
        self.index += 1

        if self.index >= len(self.images):
            self.index = 0

        if self.showing:
            self.image = self.images[self.index]
        else:
            self.image = pygame.image.load('ui/icons/blank.png')

    # deletes the image upon kill
    def delete(self, player):
        player.explosion = True
        self.kill()
        self.image = pygame.image.load('ui/icons/blank.png')
        self.showing = False

    # shake effect based on decaying cos wave
    def shake(self):
        if self.shaking:
            self.x = math.exp(-self.timex) * math.cos(15 * self.timex) * 15
            self.rect.centerx = self.pos[0] + self.x

# health bar. deals with player health
class HealthBar:
    def __init__(self, scale, pos):
        # images
        self.empty = pygame.transform.scale_by(pygame.image.load('ui/MinimalFantasy/ValueBar_128x16.png'), scale)
        self.bar = pygame.transform.scale_by(pygame.image.load('ui/MinimalFantasy/ValueRed_120x8.png'), scale)
        self.offset = pygame.math.Vector2(4, 4)

        # rect
        self.rect = self.empty.get_rect(topleft=pos)
        self.bar_rect = self.bar.get_rect(topleft=(pos[0] + self.offset.x * scale, pos[1] + self.offset.y * scale))

        # amounts
        self.amount = 100
        self.total = 100
        self.start_total = 100

        # event variables
        self.time = 0
        self.iframe_start = 0
        self.iframe_length = 500
        
        self.damageable = True

        # sounds
        self.hurt_sound = pygame.mixer.Sound('audio/Hurt.wav')

    # check for cooldown
    def update(self, player):
        self.time = pygame.time.get_ticks()

        self.total = self.start_total + player.attributes[0] * 10

        
        if self.time - self.iframe_start >= self.iframe_length:
            self.damageable = True

    def draw(self, display):
        bar_width = self.bar_rect.w * (self.amount / self.total)

        display.blit(self.empty, self.rect)
        # draws only a percentage of the full image
        display.blit(self.bar, self.bar_rect, area=(0, 0, bar_width, self.bar_rect.h))

    def damage(self, damage, player):
        # calculate defence
        temp_def = 0
        for i in range(4):
            if player.equip[i] > 0:
                temp_def += 1

        # apply damage
        if self.damageable:
            damage = damage - player.attributes[2] - temp_def
            if damage < 0:
                damage = 0
            self.amount -= damage
            if self.amount < 0:
                self.amount = 0
            self.iframe_start = self.time
            self.damageable = False
            player.hit = True
            self.hurt_sound.play()

# item for when a enemy drops one
class Item(pygame.sprite.Sprite):
    def __init__(self, pos, item_num, scale):
        pygame.sprite.Sprite.__init__(self)

        # image
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

        # rect and pos
        self.rect = self.image.get_rect(center=pos)
        self.pos = pos
        self.x = 0
        self.y = 0
        self.item_num = item_num

    # bob animation and pick up function
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

# explosion with particles
class Explosion:
    def __init__(self, pos_range, num_of_particles, size, colour, angle_range, speed_range, gravity):

        # adds particles
        self.particles = pygame.sprite.Group()
        for i in range(num_of_particles):
            self.particles.add(Particle((random.randrange(pos_range[0],
                                                          pos_range[1]),
                                         random.randrange(pos_range[2],
                                                          pos_range[3])), colour, size,
                                        random.randrange(angle_range[0], angle_range[1]),
                                        random.randrange(speed_range[0], speed_range[1]) / 1000, gravity))

    # update particles
    def update(self, dt):
        if self.particles.sprites():
            self.particles.update(dt)

    # draw particles
    def draw(self, display):
        self.particles.draw(display)


# particle engine
class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, colour, size, angle, speed, gravity):
        pygame.sprite.Sprite.__init__(self)

        # image
        self.image = pygame.Surface((size, size), pygame.SRCALPHA, 32).convert_alpha()

        # pos and movement variables
        self.time = pygame.time.get_ticks()
        self.creation = self.time
        self.time_offset = int(random.random() * 100)
        self.angle = math.radians(angle)
        self.origin = pos
        self.speed = speed
        self.gravity = gravity
        self.rect = self.image.get_rect(center=pos)
        self.colour = colour
        self.size = size

        # calculate x and y movement from angle
        self.velocity = pygame.math.Vector2(self.speed * math.sin(self.angle), self.speed * math.cos(self.angle))
        self.position = pygame.math.Vector2(self.origin[0], self.origin[1])

    # move particle
    def update(self, dt):
        self.time = pygame.time.get_ticks()
        if self.time - self.creation > self.time_offset:
            pygame.draw.circle(self.image, self.colour, (self.size / 2, self.size / 2), self.size / 2)
            self.velocity.y += self.gravity
            self.position.y += self.velocity.y * dt
            self.position.x += self.velocity.x * dt

            self.rect.x = self.position.x
            self.rect.y = self.position.y

            # delete if off screen
            if self.rect.x > WIDTH or self.rect.x < 0 or self.rect.y < 0 or self.rect.y > HEIGHT:
                self.kill()

# dummy for placeholder
class Dummy:
    def __init__(self):
        self.particles = pygame.sprite.Group()
        self.particles.add(Particle((0, 0), (0, 0, 0), 0, 0, 0, 0))

    def update(self, dummy):
        pass

    def draw(self, display):
        pass

# fade for animation
class Fade(pygame.sprite.Sprite):
    def __init__(self, alpha):
        pygame.sprite.Sprite.__init__(self)

        # image and rects
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.image.fill((0, 0, 0, alpha))
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.opacity = 0

    # fades out the screen
    def update(self, fadeout):
        if fadeout:
             self.opacity += 2
             if self.opacity > 255:
                 self.opacity = 255
                 return
             self.image.set_alpha(self.opacity)
        else:
            self.opacity += 2
            if self.opacity > 255:
                self.opacity = 255
                self.delete()
                return
            self.image.set_alpha(255 - self.opacity)


    def delete(self):
        self.kill()

