"""
--------------------------------------------------
Project: Programming and Complex Processes
Standard: 91906, 91907
School: Hauraki Plains College
Author: Noah Fieten
Date Started: 25/7/24
Python: 3.10
--------------------------------------------------
"""
import pygame
import sys
import os
import json
from enemy import Enemy
from settings import *
from player import Player
from tilemap import TileMap, spawn_enemies
from camera import Camera
from ui import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    tiles = TileMap('dungeon/', 'dungeon/')

    levels = []
    level_list = os.scandir('levels/')
    with level_list as alevel:
        for level in alevel:
            with open(level.path, 'r') as openfile:
                levels.append(json.load(openfile))

    backgrounds = []
    back_list = os.scandir('backgrounds/')
    with back_list as backs:
        for back in backs:
            with open(back.path, 'r') as openfile:
                backgrounds.append(json.load(openfile))

    current_level = 0

    border = WIDTH * 2

    player = Player(300, HEIGHT / 2 + 200, 3, border)
    player_state = 'idle'

    camera = Camera(player)

    inventory = Inventory((WIDTH / 2, HEIGHT / 2), 550, 4)
    misc_inventory = pygame.sprite.Group()
    attribute_buttons = pygame.sprite.Group()
    slots = pygame.sprite.Group()
    animations = pygame.sprite.Group()
    slot_icons = pygame.sprite.Group()
    spirit_amount = pygame.sprite.Group()
    
    misc_inventory.add(PlayerBorder(inventory, 8))

    slot_icons.add(Icon(inventory, ((WIDTH / 2) - 150, (HEIGHT / 2) + 220), pygame.image.load('ui/icons/helmet.png'), 6))
    slot_icons.add(Icon(inventory, ((WIDTH / 2) - 50, (HEIGHT / 2) + 220), pygame.image.load('ui/icons/chestplate.png'), 6))
    slot_icons.add(Icon(inventory, ((WIDTH / 2) + 50, (HEIGHT / 2) + 220), pygame.image.load('ui/icons/leggings.png'), 6))
    slot_icons.add(Icon(inventory, ((WIDTH / 2) + 150, (HEIGHT / 2) + 220), pygame.image.load('ui/icons/boots.png'), 6))
    slot_icons.add(Icon(inventory, ((WIDTH / 2), (HEIGHT / 2) + 120), pygame.image.load('ui/icons/sword.png'), 6))
    
    misc_inventory.add(Icon(inventory, (WIDTH / 2 - 5, HEIGHT / 2 - 140), pygame.image.load('misc_assets/player/tile000.png'), 14))
    
    misc_inventory.add(Icon(inventory, (250, 330), pygame.image.load('ui/icons/heart.png'), 7))
    misc_inventory.add(Icon(inventory, (250, 470), pygame.image.load('ui/icons/strength.png'), 7))
    misc_inventory.add(Icon(inventory, (250, 610), pygame.image.load('ui/icons/defense.png'), 7))
    misc_inventory.add(Icon(inventory, (250, 750), pygame.image.load('ui/icons/stamina.png'), 7))

    attribute_buttons.add(AttributeButton((560, 352), 5))
    attribute_buttons.add(AttributeButton((560, 492), 5))
    attribute_buttons.add(AttributeButton((560, 632), 5))
    attribute_buttons.add(AttributeButton((560, 772), 5))

    misc_inventory.add(UiText('Con', 'fonts/pixel.ttf', 40, (0, 0, 0), (320, 290)))
    misc_inventory.add(UiText('Str', 'fonts/pixel.ttf', 40, (0, 0, 0), (320, 430)))
    misc_inventory.add(UiText('Def', 'fonts/pixel.ttf', 40, (0, 0, 0), (320, 570)))
    misc_inventory.add(UiText('Spe', 'fonts/pixel.ttf', 40, (0, 0, 0), (320, 710)))
    
    spirit_amount.add(SpiritAmount(0, 'fonts/pixel.ttf', 20, (0, 0, 255), [(WIDTH/2 - 2, 440), (WIDTH/2 - 2, 440), (WIDTH/2 - 2, 440), (WIDTH/2 - 2, 440), (WIDTH/2 - 2, 440), (WIDTH/2 - 2, 440), (WIDTH/2 - 2, 440), (WIDTH/2 - 2, 440), (WIDTH/2 - 2, 440), (WIDTH/2 - 2, 440), (WIDTH/2 - 2, 440), (WIDTH/2 - 2, 440),]))

    attributes = [3, 5, 7, 2]
    attribute_bars = []
    attribute_bars.append(AttributeBar(inventory, (320, 330), 5))
    attribute_bars.append(AttributeBar(inventory, (320, 470), 5))
    attribute_bars.append(AttributeBar(inventory, (320, 610), 5))
    attribute_bars.append(AttributeBar(inventory, (320, 750), 5))

    
    animations.add(AnimatedImage([
        'misc_assets/spirit_fire/frame_00_delay-0.08s.png',
        'misc_assets/spirit_fire/frame_01_delay-0.08s.png',
        'misc_assets/spirit_fire/frame_02_delay-0.08s.png',
        'misc_assets/spirit_fire/frame_03_delay-0.08s.png',
        'misc_assets/spirit_fire/frame_04_delay-0.08s.png',
        'misc_assets/spirit_fire/frame_05_delay-0.08s.png',
        'misc_assets/spirit_fire/frame_06_delay-0.08s.png',
        'misc_assets/spirit_fire/frame_07_delay-0.08s.png',
        'misc_assets/spirit_fire/frame_08_delay-0.08s.png',
        'misc_assets/spirit_fire/frame_09_delay-0.08s.png',
        'misc_assets/spirit_fire/frame_10_delay-0.08s.png',
        'misc_assets/spirit_fire/frame_11_delay-0.08s.png',
        'misc_assets/spirit_fire/frame_12_delay-0.08s.png',
        'misc_assets/spirit_fire/frame_13_delay-0.08s.png',
        'misc_assets/spirit_fire/frame_14_delay-0.08s.png',
        'misc_assets/spirit_fire/frame_15_delay-0.08s.png',
        'misc_assets/spirit_fire/frame_16_delay-0.08s.png',
        'misc_assets/spirit_fire/frame_17_delay-0.08s.png',
        'misc_assets/spirit_fire/frame_18_delay-0.08s.png',
        'misc_assets/spirit_fire/frame_19_delay-0.08s.png',
        'misc_assets/spirit_fire/frame_20_delay-0.08s.png',
        'misc_assets/spirit_fire/frame_21_delay-0.08s.png',
        'misc_assets/spirit_fire/frame_22_delay-0.08s.png',
        'misc_assets/spirit_fire/frame_23_delay-0.08s.png',
        'misc_assets/spirit_fire/frame_24_delay-0.08s.png',
        'misc_assets/spirit_fire/frame_25_delay-0.08s.png',
        'misc_assets/spirit_fire/frame_26_delay-0.08s.png',
        'misc_assets/spirit_fire/frame_27_delay-0.08s.png'], (WIDTH / 2, HEIGHT / 2 - 170), 3, False, False, camera, True))

    for i in range(24):
        slots.add(InventorySlot(inventory, i, 4.5))
    for i in range(5):
        slots.add(EquipSlot(inventory, i + 1, 4.5))

    enemies = pygame.sprite.Group()

    NEW_PLAYER_FRAME = pygame.USEREVENT
    pygame.time.set_timer(NEW_PLAYER_FRAME, 150)
    FIRE_ANIM = pygame.USEREVENT + 1
    #pygame.time.set_timer(FIRE_ANIM, 80)
    ENEMY_ANIM = pygame.USEREVENT + 2
    pygame.time.set_timer(ENEMY_ANIM, 150)
    SMOKE_ANIM = pygame.USEREVENT + 3
    pygame.time.set_timer(SMOKE_ANIM, 40)
    FLAME_ANIM = pygame.USEREVENT + 4
    pygame.time.set_timer(FLAME_ANIM, 300)
    
    loading = 0

    running = True
    while running:

        # delta time - so player speed will look the same no matter the frame rate
        if loading <= 2:
            loading = False
            dt = 1
        elif loading > 2:
            dt = clock.tick(60) * 0.001 * TARGET_FPS
            
        loading += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    
                if not inventory.showing:
                    if event.key == pygame.K_LEFT:
                        player.turn(True)
                        player.RIGHT_KEY = False
                        player.LEFT_KEY, player.FACING_LEFT = True, True
                    elif event.key == pygame.K_RIGHT:
                        player.turn(False)
                        player.LEFT_KEY = False
                        player.RIGHT_KEY, player.FACING_LEFT = True, False
                    elif event.key == pygame.K_z:
                        player.jump()

                    if event.key == pygame.K_x:
                        player.attack(camera)
                    if event.key == pygame.K_s:
                        enemies = spawn_enemies([(200, HEIGHT / 2), (400, HEIGHT / 2)])

                if event.key == pygame.K_i:
                    if inventory.showing:
                        inventory.showing = False
                    else:
                        inventory.showing = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.LEFT_KEY = False
                elif event.key == pygame.K_RIGHT:
                    player.RIGHT_KEY = False
                elif event.key == pygame.K_z:
                    if player.is_jumping:
                        player.velocity.y *= 0.25
                        player.is_jumping = False


            if not inventory.showing:
                if event.type == NEW_PLAYER_FRAME:
                    player.update_frame(player.state)
            
            if event.type == FIRE_ANIM:
                animations.update(camera)
                spirit_amount.update(player.spirit)

            if event.type == ENEMY_ANIM:
                if enemies.sprites():
                    for sprite in enemies.sprites():
                        sprite.update_frame()

            if event.type == SMOKE_ANIM:
                player.poof.update(camera)

            if event.type == FLAME_ANIM:
                if player.flame.sprites():
                    for flame in player.flame.sprites():
                        flame.update_frame()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for slot in slots.sprites():
                    slot.drag(inventory)
            if event.type == pygame.MOUSEBUTTONUP:
                for slot in slots.sprites():
                    slot.drop(inventory)

                if inventory.moving_slot != -1:
                    inventory.moving_slot = -1



        
        if not inventory.showing:
            if player.RIGHT_KEY:
                if not player_state == 'run':
                    player_state = 'run'
                    player.update_frame('run_right')

            elif player.LEFT_KEY:
                if not player_state == 'run':
                    player_state = 'run'
                    player.update_frame('run_left')
            else:
                if not player_state == 'idle':
                    if player.FACING_LEFT:
                        player.update_frame('idle_left')
                        player_state = 'idle'
                    else:
                        player.update_frame('idle_right')
                        player_state = 'idle'



        if player.rect.x > WIDTH - player.rect.w:
            enemies.empty()
            match current_level:
                case 0:
                    current_level = 1
                    player.position = pygame.math.Vector2(0, HEIGHT / 2 + 200)
                    player.velocity.y = 0
                    camera.offset_float = 0
                    camera.offset = 0
                    border = WIDTH * 2

                    enemies = spawn_enemies([(1128, 800), (764, 800), (3087, 800), (2823, 800), (2588, 800)])
                case 1:
                    current_level = 2
                    player.position = pygame.math.Vector2(0, HEIGHT / 2 + 200)
                    player.velocity.y = 0
                    camera.offset_float = 0
                    camera.offset = 0
                    border = WIDTH * 2

                    enemies = spawn_enemies([(994, 800), (3193, 760)])
                case 2:
                    current_level = 3
                    player.position = pygame.math.Vector2(0, HEIGHT / 2 + 240)
                    player.velocity.y = 0
                    camera.offset_float = 0
                    camera.offset = 0
                    border = WIDTH
                case 3:
                    current_level = 8
                    player.position = pygame.math.Vector2(0, HEIGHT / 2 + 200)
                    player.velocity.y = 0
                    camera.offset_float = 0
                    camera.offset = 0
                    border = WIDTH
                case 5:
                    current_level = 4
                    player.position = pygame.math.Vector2(0, HEIGHT / 2 + 240)
                    player.velocity.y = 0
                    camera.offset_float = 0
                    camera.offset = 0
                    border = WIDTH
                case 6:
                    current_level = 5
                    player.position = pygame.math.Vector2(0, HEIGHT / 2 + 200)
                    player.velocity.y = 0
                    camera.offset_float = 0
                    camera.offset = 0
                    border = WIDTH * 2

                    enemies = spawn_enemies([(871, 920), (1092, 920), (1336, 920), (1130, 920), (933, 920), (689, 920), (411, 920)])
                case 8:
                    print("END")
                case _:
                    pass

        elif player.rect.x < 0:
            enemies.empty()
            match current_level:
                case 1:
                    current_level = 0
                    player.position = pygame.math.Vector2(WIDTH * 2 - player.rect.w, HEIGHT / 2 + 200)
                    player.velocity.y = 0
                    camera.offset_float = WIDTH
                    camera.offset = WIDTH
                    border = WIDTH * 2
                case 2:
                    current_level = 1
                    player.position = pygame.math.Vector2(WIDTH * 2 - player.rect.w, HEIGHT / 2 + 200)
                    player.velocity.y = 0
                    camera.offset_float = WIDTH
                    camera.offset = WIDTH
                    border = WIDTH * 2

                    enemies = spawn_enemies([(1128, 800), (764, 800), (3087, 800), (2823, 800), (2588, 800)])
                case 3:
                    current_level = 2
                    player.position = pygame.math.Vector2(WIDTH * 2 - player.rect.w, HEIGHT / 2 + 240)
                    player.velocity.y = 0
                    camera.offset_float = WIDTH
                    camera.offset = WIDTH
                    border = WIDTH * 2

                    enemies = spawn_enemies([(994, 800), (3193, 760)])
                case 4:
                    current_level = 5
                    player.position = pygame.math.Vector2(WIDTH * 2 - player.rect.w, HEIGHT / 2 + 240)
                    player.velocity.y = 0
                    camera.offset_float = WIDTH
                    camera.offset = WIDTH
                    border = WIDTH * 2

                    enemies = spawn_enemies([(871, 920), (1092, 920), (1336, 920), (1130, 920), (933, 920), (689, 920), (411, 920)])
                case 5:
                    current_level = 6
                    player.position = pygame.math.Vector2(WIDTH - player.rect.w, HEIGHT / 2 + 200)
                    player.velocity.y = 0
                    camera.offset_float = WIDTH
                    camera.offset = WIDTH
                    border = WIDTH
                case 8:
                    current_level = 3
                    player.position = pygame.math.Vector2(WIDTH - player.rect.w, HEIGHT / 2 + 280)
                    player.velocity.y = 0
                    camera.offset_float = 0
                    camera.offset = 0
                    border = WIDTH
                case _:
                    pass

        elif player.rect.y > HEIGHT:
            enemies.empty()
            match current_level:
                case 3:
                    current_level = 10
                    player.position = pygame.math.Vector2(870, player.rect.h)
                    camera.offset = 0
                    border = WIDTH
                case 4:
                    current_level = 3
                    player.position = pygame.math.Vector2(180, player.rect.h)
                    camera.offset_float = 0
                    border = WIDTH
                case 6:
                    current_level = 7
                    player.position = pygame.math.Vector2(864, player.rect.h)
                    camera.offset = 0
                    border = WIDTH

                    enemies = spawn_enemies([(1548, 920), (514, 920), (155, 920)])
                case 9:
                    current_level = 2
                    player.position = pygame.math.Vector2(WIDTH + 120, player.rect.h)
                    camera.offset_float = 1230.0
                    camera.offset = 1230
                    
                    border = WIDTH * 2
                case _:
                    pass

        elif player.rect.y < 0:
            enemies.empty()
            match current_level:
                case 2:
                    current_level = 9
                    player.position = pygame.math.Vector2(WIDTH / 2 - 150, HEIGHT)
                    player.velocity.y = -10
                    camera.offset = 0
                    border = WIDTH
                case 3:
                    current_level = 4
                    player.position = pygame.math.Vector2(880, HEIGHT)
                    player.velocity.y = -10
                    camera.offset = 0
                    border = WIDTH
                case 10:
                    current_level = 3
                    player.position = pygame.math.Vector2(970, HEIGHT)
                    player.velocity.y = -15
                    camera.offset = 0
                    border = WIDTH
                case _:
                    pass
                    

        screen.fill((0, 0, 0))

        tile_rects1, spike_rects1 = tiles.draw(screen, levels[current_level * 2], 0, 0, backgrounds[0], 9, camera)
        tile_rects2, spike_rects2 = tiles.draw(screen, levels[current_level * 2 + 1], 1, 0, backgrounds[0], 9, camera)

        tile_rects = tile_rects1 + tile_rects2
        spike_rects = spike_rects1 + spike_rects2
        
        player.update(dt, tile_rects, spike_rects, border, camera, inventory.showing, enemies.sprites())
        camera.scroll()
        
        player.draw(screen)

        if not inventory.showing:
            enemies.update(dt, camera, tile_rects)
        enemies.draw(screen)



        inventory.draw(screen)
        if inventory.showing:
            slots.draw(screen)
            misc_inventory.draw(screen)
            
            for i in range(5):
                if inventory.equip[i] == 0:
                    slot_icons.sprites()[i].draw(screen)

            attribute_buttons.draw(screen)
            j = 0
            for i in attribute_bars:
                i.draw(screen, attributes[j])
                j += 1
            animations.draw(screen)
            slots.update(inventory, screen)
            spirit_amount.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()
