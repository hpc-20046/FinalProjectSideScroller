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
# imports
import pygame
import sys
import os
import json
from settings import *
from player import Player
from tilemap import TileMap, spawn_enemies
from camera import Camera
from ui import *

# play again variable
play_again = True


def main():
    # pygame init, setting screen, and clock
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    
    # declaring time and play again variable
    time = 1
    global play_again
    play_again = False

    # loading tilemap and levels into list
    tiles = TileMap('dungeon/')

    levels = []
    level_list = os.scandir('levels/')
    with level_list as alevel:
        for level in alevel:
            with open(level.path, 'r') as openfile:
                levels.append(json.load(openfile))
                
    # level variables
    current_level = 0
    border = WIDTH * 2

    # load player object and state
    player = Player(300, HEIGHT / 2 + 200, 3, border)
    player_state = 'idle'

    # load camera object
    camera = Camera(player)

    # creating inventory and other visual groups
    inventory = Inventory((WIDTH / 2, HEIGHT / 2), 550, 4)
    misc_inventory = pygame.sprite.Group()
    attribute_buttons = pygame.sprite.Group()
    slots = pygame.sprite.Group()
    animations = pygame.sprite.Group()
    slot_icons = pygame.sprite.Group()
    spirit_amount = pygame.sprite.Group()
    tutorial_text = pygame.sprite.Group()
    level_animations = pygame.sprite.Group()
    

    # adding inventory backgrounds
    misc_inventory.add(PlayerBorder(inventory, 8))

    # adding equip slot icons
    slot_icons.add(Icon(inventory, ((WIDTH / 2) - 150, (HEIGHT / 2) + 220), pygame.image.load('ui/icons/helmet.png'), 6))
    slot_icons.add(Icon(inventory, ((WIDTH / 2) - 50, (HEIGHT / 2) + 220), pygame.image.load('ui/icons/chestplate.png'), 6))
    slot_icons.add(Icon(inventory, ((WIDTH / 2) + 50, (HEIGHT / 2) + 220), pygame.image.load('ui/icons/leggings.png'), 6))
    slot_icons.add(Icon(inventory, ((WIDTH / 2) + 150, (HEIGHT / 2) + 220), pygame.image.load('ui/icons/boots.png'), 6))
    slot_icons.add(Icon(inventory, ((WIDTH / 2), (HEIGHT / 2) + 120), pygame.image.load('ui/icons/sword.png'), 6))
    
    # adding translucent player in the middle of the inventory
    misc_inventory.add(Icon(inventory, (WIDTH / 2 - 5, HEIGHT / 2 - 140), pygame.image.load('misc_assets/player/tile000.png'), 14))
    
    # adding attribute icons
    misc_inventory.add(Icon(inventory, (250, 330), pygame.image.load('ui/icons/heart.png'), 7))
    misc_inventory.add(Icon(inventory, (250, 470), pygame.image.load('ui/icons/strength.png'), 7))
    misc_inventory.add(Icon(inventory, (250, 610), pygame.image.load('ui/icons/defense.png'), 7))
    misc_inventory.add(Icon(inventory, (250, 750), pygame.image.load('ui/icons/stamina.png'), 7))

    # adding attribute buttons
    attribute_buttons.add(AttributeButton((560, 352), 5, 0))
    attribute_buttons.add(AttributeButton((560, 492), 5, 1))
    attribute_buttons.add(AttributeButton((560, 632), 5, 2))
    attribute_buttons.add(AttributeButton((560, 772), 5, 3))

    # adding attribute text
    misc_inventory.add(UiText('Con', 'fonts/pixel.ttf', 40, (0, 0, 0), (320, 290)))
    misc_inventory.add(UiText('Str', 'fonts/pixel.ttf', 40, (0, 0, 0), (320, 430)))
    misc_inventory.add(UiText('Def', 'fonts/pixel.ttf', 40, (0, 0, 0), (320, 570)))
    misc_inventory.add(UiText('Spe', 'fonts/pixel.ttf', 40, (0, 0, 0), (320, 710)))
    
    # adding floating number showing your spirit amount
    spirit_amount.add(SpiritAmount(0, 'fonts/pixel.ttf', 20, (0, 0, 255), [
        (WIDTH/2 - 2, 440), (WIDTH/2 - 2, 440), (WIDTH/2 - 2, 445), (WIDTH/2 - 2, 450), (WIDTH/2 - 2, 450),
        (WIDTH/2 - 2, 455), (WIDTH/2 - 2, 455), (WIDTH/2 - 2, 460), (WIDTH/2 - 2, 465), (WIDTH/2 - 2, 465),
        (WIDTH/2 - 2, 465), (WIDTH/2 - 2, 465), (WIDTH/2 - 2, 465), (WIDTH/2 - 2, 460), (WIDTH/2 - 2, 460),
        (WIDTH/2 - 2, 455), (WIDTH/2 - 2, 450), (WIDTH/2 - 2, 450), (WIDTH/2 - 2, 445), (WIDTH/2 - 2, 445),
        (WIDTH/2 - 2, 445), (WIDTH/2 - 2, 440), (WIDTH/2 - 2, 440), (WIDTH/2 - 2, 440), (WIDTH/2 - 2, 440),
        (WIDTH/2 - 2, 440), (WIDTH/2 - 2, 440), (WIDTH/2 - 2, 440)
    ]))

    # added attribute bars
    attribute_bars = []
    attribute_bars.append(AttributeBar(inventory, (320, 330), 5))
    attribute_bars.append(AttributeBar(inventory, (320, 470), 5))
    attribute_bars.append(AttributeBar(inventory, (320, 610), 5))
    attribute_bars.append(AttributeBar(inventory, (320, 750), 5))

    # added tutorial text on each level
    tutorial_text.add(TutorialText('ARROW KEYS to move', 'fonts/pixel.ttf', 40, (255, 255, 255), (200, 100), 0))
    tutorial_text.add(TutorialText('Z to jump', 'fonts/pixel.ttf', 40, (255, 255, 255), (200, 160), 0))
    tutorial_text.add(TutorialText('SPIKES can kill you', 'fonts/pixel.ttf', 40, (255, 255, 255), (WIDTH + 800, 160), 0))

    tutorial_text.add(TutorialText('X to attack', 'fonts/pixel.ttf', 40, (255, 255, 255), (900, 400), 1))
    tutorial_text.add(TutorialText('enemies will drop SPIRIT', 'fonts/pixel.ttf', 40, (255, 255, 255), (WIDTH + 500, 100), 1))
    tutorial_text.add(TutorialText('use SPIRIT to UPGRADE', 'fonts/pixel.ttf', 40, (255, 255, 255), (WIDTH + 500, 200), 1))
    tutorial_text.add(TutorialText('your character and open DOORS', 'fonts/pixel.ttf', 40, (255, 255, 255), (WIDTH + 500, 260), 1))

    tutorial_text.add(TutorialText('I to open inventory', 'fonts/pixel.ttf', 40, (255, 255, 255), (300, 400), 2))
    tutorial_text.add(TutorialText('this is where you EQUIP items,', 'fonts/pixel.ttf', 40, (255, 255, 255), (1000, 500), 2))
    tutorial_text.add(TutorialText('UPGRADE you character, and see your SPIRIT', 'fonts/pixel.ttf', 40, (255, 255, 255), (1000, 560), 2))
    tutorial_text.add(TutorialText('UPGRADES use SPIRIT', 'fonts/pixel.ttf', 40, (255, 255, 255), (WIDTH + 500, 300), 2))

    # added spirit fire to rhe center of the inventory
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

    # added beating heart on level 8
    level_animations.add(AnimatedLevelImage([
        'misc_assets/heart/frame_0_delay-0.1s.png',
        'misc_assets/heart/frame_1_delay-0.1s.png',
        'misc_assets/heart/frame_2_delay-0.1s.png',
        'misc_assets/heart/frame_3_delay-0.1s.png',
        'misc_assets/heart/frame_4_delay-0.1s.png',
        'misc_assets/heart/frame_5_delay-0.1s.png',
        'misc_assets/heart/frame_5_delay-0.1s.png',
        'misc_assets/heart/frame_5_delay-0.1s.png',
        'misc_assets/heart/frame_5_delay-0.1s.png',
        'misc_assets/heart/frame_5_delay-0.1s.png',
        'misc_assets/heart/frame_5_delay-0.1s.png',
        'misc_assets/heart/frame_5_delay-0.1s.png',
        'misc_assets/heart/frame_5_delay-0.1s.png',
        'misc_assets/heart/frame_5_delay-0.1s.png',
        'misc_assets/heart/frame_5_delay-0.1s.png',
        'misc_assets/heart/frame_5_delay-0.1s.png',
        'misc_assets/heart/frame_5_delay-0.1s.png',
        'misc_assets/heart/frame_5_delay-0.1s.png',
        'misc_assets/heart/frame_5_delay-0.1s.png',
        'misc_assets/heart/frame_5_delay-0.1s.png'
    ], (980, 700), 0.3, 7, True, 10))
    

    # added door at the end of the level
    door_surf = pygame.transform.scale_by(pygame.image.load('ui/Level_0__Tiles.png'), 2.5)
    door_rect = door_surf.get_rect(topright=(WIDTH, 14*40))
    
    # init the sounds for inventory
    inventory_in = pygame.mixer.Sound('audio/Menu_In.wav')
    inventory_out = pygame.mixer.Sound('audio/Menu_Out.wav')


    # adding inventory and equip slots
    for i in range(24):
        slots.add(InventorySlot(inventory, i, 4.5))
    for i in range(5):
        slots.add(EquipSlot(inventory, i + 1, 4.5))
    
    # added health bar
    health_bar = HealthBar(2.5, (60, HEIGHT - 80))

    # init visuals for animation
    explosion = Dummy()
    fade = pygame.sprite.Group()
    fadeout = True
    fade_text = pygame.Surface((0,0))
    fade_rect = fade_text.get_rect(topleft=(0, 0))
    fade_time = 0
    fade_anim = False
    
    # adding fonts and text for main menu
    dungeon_font = pygame.font.Font('fonts/DungeonFont.ttf', 80)
    title_font = pygame.font.Font('fonts/DungeonFont.ttf', 120)
    button_font = pygame.font.Font('fonts/DungeonFont.ttf', 60)

    title_text = title_font.render('Main Title', True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(WIDTH / 2, 300))

    start_text = button_font.render('start', True, (255, 255, 255))
    start_rect = start_text.get_rect(center=(WIDTH / 2, 600))

    options_text = button_font.render('options', True, (255, 255, 255))
    options_rect = options_text.get_rect(center=(WIDTH / 2, 700))

    quit_text = button_font.render('quit', True, (255, 255, 255))
    quit_rect = quit_text.get_rect(center=(WIDTH / 2, 800))

    # init enemy group
    enemies = pygame.sprite.Group()

    # init sounds for menu theme
    title_sound = pygame.mixer.Sound('audio/title.wav')
    music = pygame.mixer.Sound('audio/(Loop) Powerful Relic Theme.wav')
    music.play(-1)
    music.set_volume(0.6)

    # setting intervals for custom events
    NEW_PLAYER_FRAME = pygame.USEREVENT
    pygame.time.set_timer(NEW_PLAYER_FRAME, 150)
    FIRE_ANIM = pygame.USEREVENT + 1
    pygame.time.set_timer(FIRE_ANIM, 80)
    ENEMY_ANIM = pygame.USEREVENT + 2
    pygame.time.set_timer(ENEMY_ANIM, 150)
    SMOKE_ANIM = pygame.USEREVENT + 3
    pygame.time.set_timer(SMOKE_ANIM, 40)
    FLAME_ANIM = pygame.USEREVENT + 4
    pygame.time.set_timer(FLAME_ANIM, 300)
    HEART_ANIM = pygame.USEREVENT + 5
    pygame.time.set_timer(HEART_ANIM, 100)
    ROLL_ANIM = pygame.USEREVENT + 6
    pygame.time.set_timer(ROLL_ANIM, 50)
    HIT_ANIM = pygame.USEREVENT + 7
    pygame.time.set_timer(HIT_ANIM, 150)
    
    # variable so computers sucky specs don't ruin the spawn point
    loading = 0

    # game states
    running = True
    main_menu = True
    game_over = False
    end_game = True

    # menu screen loop
    while main_menu:

        # event loop
        for event in pygame.event.get():
            # quitting the game
            if event.type == pygame.QUIT:
                running = False
                main_menu = False
                end_game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    main_menu = False
                    end_game = False

            # check for mouse clicks on the buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(pygame.mouse.get_pos()):
                    main_menu = False
                elif options_rect.collidepoint(pygame.mouse.get_pos()):
                    options_text = button_font.render('lol theres no options', True, (255, 255, 255))
                    options_rect = options_text.get_rect(center=(WIDTH / 2, 700))
                elif quit_rect.collidepoint(pygame.mouse.get_pos()):
                    main_menu = False
                    running = False
                    end_game = False

        # reset screen
        screen.fill((0, 0, 0))

        # draw text and buttons
        screen.blit(title_text, title_rect)
        screen.blit(start_text, start_rect)
        screen.blit(options_text, options_rect)
        screen.blit(quit_text, quit_rect)

        # update display
        pygame.display.flip()

    # change game music
    music.fadeout(500)
    music = pygame.mixer.Sound('audio/(Loop) Forest Exploration.wav')
    music.play(-1)
    music.set_volume(0.6)

    # main loop
    while running:

        # set the time for intervals
        time = pygame.time.get_ticks()

        # delta time - so player speed will look the same no matter the frame rate
        if loading <= 2:
            loading = False
            dt = 1
        elif loading > 2:
            dt = clock.tick(60) * 0.001 * TARGET_FPS
            
        loading += 1

        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                end_game = False
            if event.type == pygame.KEYDOWN:
                # detect arrow key pressed. only when not in inventory, alive, or not in the animation
                if not inventory.showing:
                    if not player.dead and not fade_anim and not player.animation:
                        if event.key == pygame.K_LEFT:
                            player_state = player.turn(True, player_state)
                            player.right_key = False
                            player.left_key, player.facing_left = True, True
                        elif event.key == pygame.K_RIGHT:
                            player_state = player.turn(False, player_state)
                            player.left_key = False
                            player.right_key, player.facing_left = True, False
                        elif event.key == pygame.K_z:
                            player.jump()

                        # detect key presses for jump, attack, and dash
                        if event.key == pygame.K_x:
                            player.attack()
                        if event.key == pygame.K_c:
                            player.roll()
                    else:
                        player.left_key, player.right_key = False, False

                # open the inventory when pressed i and play sound
                if event.key == pygame.K_i:
                    if not fade_anim and not player.animation:
                        if inventory.showing:
                            inventory.showing = False
                            inventory_out.play()
                        else:
                            inventory.showing = True
                            inventory_in.play()

            # detect keyup to stop movement or jump 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.left_key = False
                elif event.key == pygame.K_RIGHT:
                    player.right_key = False
                elif event.key == pygame.K_z:
                    if player.is_jumping:
                        player.velocity.y *= 0.25
                        player.is_jumping = False

            # update the player frame
            if not inventory.showing:
                if event.type == NEW_PLAYER_FRAME:
                    # play waking up animation
                    if player.animation:
                        if player.alternate_1 >= 6:
                            player.alternate_1 = 0
                            player.animation_counter -= 1
                            if player.animation_counter < 0:
                                player.animation = False
                                player_state = player.update_frame(player.state, False, False, player_state)
                            else:
                                player.image = player.death_right_frames[player.animation_counter]
                        else:
                            player.alternate_1 += 1
                    # update player image based on the player state
                    else:
                        player_state = player.update_frame(player.state, False, False, player_state)
                    
            # update the image for the spirit fire and the spirit number in the inventory
            if event.type == FIRE_ANIM:
                animations.update(camera)
                spirit_amount.update(player.spirit)

            # update the image for the enemies
            if event.type == ENEMY_ANIM:
                if enemies.sprites():
                    for sprite in enemies.sprites():
                        sprite.update_frame()

            # update the image for and poof animations happening in the level
            if event.type == SMOKE_ANIM:
                player.poof.update(camera)

            # update the image for any spirit flames in the level
            if event.type == FLAME_ANIM:
                if player.flame.sprites():
                    for flame in player.flame.sprites():
                        flame.update_frame()

            # update the image for the beating heart in level 8
            if event.type == HEART_ANIM:
                if level_animations.sprites():
                    level_animations.sprites()[0].update_frame()

            # update the player image if in a roll animation
            if event.type == ROLL_ANIM:
                player_state = player.update_frame("roll", True, False, player_state)

            # update the player image if in a hurt animation
            if event.type == HIT_ANIM:
                player_state = player.update_frame("hit", False, True, player_state)

            # check for mouse clicks on inventory and equip slots
            if event.type == pygame.MOUSEBUTTONDOWN:
                for slot in slots.sprites():
                    slot.drag(inventory)
                for button in attribute_buttons.sprites():
                    button.click(player)

            # check for when the player releases the mouse button to dop the item
            if event.type == pygame.MOUSEBUTTONUP:
                for slot in slots.sprites():
                    slot.drop(inventory)

                if inventory.moving_slot != -1:
                    inventory.moving_slot = -1
                elif inventory.moving_equip_slot != -1:
                    inventory.moving_equip_slot = -1

            # check for game over event
            if event.type == pygame.USEREVENT + 8:
                game_over = True
                running = False



        # update the player_state variable and the player image whenever there is a change in state
        if not inventory.showing:
            if not player.dead:
                if player.right_key:
                    if not player_state == 'run':
                        player_state = 'run'
                        player_state = player.update_frame('run_right', False, False, player_state)

                elif player.left_key:
                    if not player_state == 'run':
                        player_state = 'run'
                        player_state = player.update_frame('run_left', False, False, player_state)
                else:
                    if not player_state == 'idle':
                        if player.facing_left:
                            player.update_frame('idle_left', False, False, player_state)
                            player_state = 'idle'
                        else:
                            player.update_frame('idle_right', False, False, player_state)
                            player_state = 'idle'

        # stop the player moving when the animation is player or if the player is dead
        if player.dead or player.animation:
            player.left_key, player.right_key = False, False

        # check if the player exits the screen on the right side and transitions level
        if player.rect.x > WIDTH - player.rect.w:
            # deletes all the enemies, items, and spirit flames
            enemies.empty()
            player.flame.empty()
            player.item.empty()
            # check for level and update variables and spawn enemies based on the position and enemy type
            match current_level:
                case 0:
                    current_level = 1
                    player.position = pygame.math.Vector2(0, HEIGHT / 2 + 200)
                    player.velocity.y = 0
                    camera.offset_float = 0
                    camera.offset = 0
                    border = WIDTH * 2

                    enemies = spawn_enemies([(1128, 800), (764, 800), (3087, 800), (2823, 800), (2588, 800)],
                                            [1, 1, 1, 1, 1])
                case 1:
                    current_level = 2
                    player.position = pygame.math.Vector2(0, HEIGHT / 2 + 200)
                    player.velocity.y = 0
                    camera.offset_float = 0
                    camera.offset = 0
                    border = WIDTH * 2

                    enemies = spawn_enemies([(994, 800), (3193, 760)], [2, 1])
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

                    enemies = spawn_enemies([(871, 920), (1092, 920), (1336, 920),
                                             (1130, 920), (933, 920), (689, 920), (411, 920)],
                                            [1, 1, 3, 1, 1, 3, 1])
                case 8:
                    running = False
                case _:
                    pass

        # check if the player exits the screen on the left side and transitions level
        elif player.rect.x < 0:
            # deletes all the enemies, items, and spirit flames
            enemies.empty()
            player.flame.empty()
            player.item.empty()
            # check for level and update variables and spawn enemies
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

                    enemies = spawn_enemies([(1128, 800), (764, 800), (3087, 800), (2823, 800), (2588, 800)],
                                            [1, 1, 1, 1, 1])
                case 3:
                    current_level = 2
                    player.position = pygame.math.Vector2(WIDTH * 2 - player.rect.w, HEIGHT / 2 + 240)
                    player.velocity.y = 0
                    camera.offset_float = WIDTH
                    camera.offset = WIDTH
                    border = WIDTH * 2

                    enemies = spawn_enemies([(994, 800), (3193, 760)], [1, 1])
                case 4:
                    current_level = 5
                    player.position = pygame.math.Vector2(WIDTH * 2 - player.rect.w, HEIGHT / 2 + 240)
                    player.velocity.y = 0
                    camera.offset_float = WIDTH
                    camera.offset = WIDTH
                    border = WIDTH * 2

                    enemies = spawn_enemies([(871, 920), (1092, 920), (1336, 920),
                                             (1130, 920), (933, 920), (689, 920), (411, 920)],
                                            [1, 1, 3, 1, 1, 3, 1])
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

        # check if the player exits the screen on the bottom side and transitions level
        elif player.rect.y > HEIGHT:
            # deletes all the enemies, items, and spirit flames
            enemies.empty()
            player.flame.empty()
            player.item.empty()
            # check for level and update variables and spawn enemies
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
                    player.position = pygame.math.Vector2(400, player.rect.h)
                    camera.offset = 0
                    border = WIDTH

                    enemies = spawn_enemies([(1548, 920), (514, 920), (155, 920)], [1, 1, 1])
                case 9:
                    current_level = 2
                    player.position = pygame.math.Vector2(WIDTH + 120, player.rect.h)
                    camera.offset_float = 1230.0
                    camera.offset = 1230
                    
                    border = WIDTH * 2
                case _:
                    pass

        # check if the player exits the screen on the top side and transitions level
        elif player.rect.y < 0:
            # deletes all the enemies, items, and spirit flames
            enemies.empty()
            player.flame.empty()
            player.item.empty()
            # check for level and update variables and spawn enemies
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
                    
        # resets the screen to draw
        screen.fill((0, 0, 0))

        # draws all the tiles on the screen from a json file based on the camera offset and then stores the rects in a list
        tile_rects1, spike_rects1 = tiles.draw(screen, levels[current_level * 2], 0, 0, 9, camera)
        tile_rects2, spike_rects2 = tiles.draw(screen, levels[current_level * 2 + 1], 1, 0, 9, camera)

        # draws the door if on level 4 and if the door is closed
        door = []
        if current_level == 3 and player.door:
            door.append(door_rect)
            screen.blit(door_surf, door_rect)

        # fades out the music on the level with the beating heart.
        if current_level == 7:
            music.fadeout(1000)

        # combines the tile and door rects, and the spike rects into one list
        tile_rects = tile_rects1 + tile_rects2 + door
        spike_rects = spike_rects1 + spike_rects2

        # update the tutorial text based on the current level and the camera offset
        tutorial_text.update(camera, current_level)

        # start the explosion animation
        if player.explosion:
            player.explosion = False
            fadeout = True
            fade_anim = True
            fade.add(Fade(0))
            explosion = Explosion((int(WIDTH / 2 - 10 + 20), int(WIDTH / 2 + 10 + 20), int(HEIGHT / 2 - 10 + 160), int(HEIGHT / 2 + 10 + 160)),
                                  200, 10,(255, 0, 0), (0, 360), (3000, 8000), 0)

        # change level and draw the wind dash text
        if not explosion.particles.sprites():
            current_level = 0
            player.position = pygame.math.Vector2(300, HEIGHT / 2 + 200)
            player.velocity.y = 0
            camera.offset_float = 0
            camera.offset = 0
            border = WIDTH * 2
            enemies.empty()
            explosion = Dummy()
            player.power = True
            player.facing_left = False
            tutorial_text.empty()
            tutorial_text.add(TutorialText('C to dash', 'fonts/pixel.ttf', 40, (255, 255, 255),
                                           (500, 100), 0))

            fade_time = time
            fade_text = dungeon_font.render('You have acquired Wind Dash', True, (255, 255, 255))
            fade_rect = fade_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            title_sound.play()


        # fade into the level after a certain amount of time and play player animation
        if (time - fade_time > 5000) and fade_time != 0:
            fade.empty()
            fade_text = dungeon_font.render('', True, (255, 255, 255))
            fade.add(Fade(255))
            fade_time = 0
            fadeout = False
            fade_anim = False
            player.animation = True
            pygame.event.post(pygame.event.Event(NEW_PLAYER_FRAME))
            music.play(-1)

        # make it so the enemies only move when you are not in the inventory
        if not inventory.showing:
            enemies.update(dt, camera, tile_rects, health_bar, player)

        # update the level animations
        level_animations.update(current_level, player)

        # update the health bar
        health_bar.update(player)

        # update the particle explosion and the fade
        explosion.update(dt)
        fade.update(fadeout)

        # update the player
        player.update(dt, tile_rects, spike_rects, border, camera, inventory, enemies.sprites(), health_bar, current_level)

        # update the camera offset
        camera.scroll()

        # draw the tutorial text
        tutorial_text.draw(screen)

        # draw the level animations
        level_animations.draw(screen)

        # draw the player
        player.draw(screen)

        # draw the enemies
        enemies.draw(screen)

        # draw the inventory
        inventory.draw(screen)

        # draw everything in the inventory if it is showing
        if inventory.showing:
            slots.draw(screen)
            misc_inventory.draw(screen)
            
            for i in range(5):
                if inventory.equip[i] == 0:
                    slot_icons.sprites()[i].draw(screen)

            attribute_buttons.draw(screen)
            j = 0
            for i in attribute_bars:
                i.draw(screen, player.attributes[j])
                j += 1
            animations.draw(screen)
            slots.update(inventory, screen)
            spirit_amount.draw(screen)
        else:
            # draw the health bar when not in the inventory
            health_bar.draw(screen)

        # draw the fade
        fade.draw(screen)

        # draw the wind dash text
        screen.blit(fade_text, fade_rect)

        # draw the particles in the explosion
        explosion.draw(screen)

        # update the screen
        pygame.display.flip()
        # tick the clock at 60 fps
        clock.tick(60)

    # fade out the music when died or finished the game
    music.fadeout(1000)

    # set game over title and buttons
    game_over_title = title_font.render('You Died', True, (255, 255, 255))
    game_over_rect = game_over_title.get_rect(center=(WIDTH / 2, 200))

    play_again_text = button_font.render('play again', True, (255, 255, 255))
    play_again_rect = play_again_text.get_rect(center=(WIDTH / 2 - 200, 900))

    end_quit_text = button_font.render('quit', True, (255, 255, 255))
    end_quit_rect = end_quit_text.get_rect(center=(WIDTH / 2 + 200, 900))

    # set the player image
    dead_image = pygame.transform.scale_by(pygame.image.load('player/death/right/tile075.png'), 3)
    dead_rect = dead_image.get_rect(center=(WIDTH / 2, HEIGHT / 2))

    # game over loop
    while game_over:

        # make sure that when you quit or play again, it doesn't go to the win screen
        end_game = False

        # event loop
        for event in pygame.event.get():
            # quit the game
            if event.type == pygame.QUIT:
                end_game = False
                game_over = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    end_game = False
                    game_over = False

            # check for mouse click on buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                if end_quit_rect.collidepoint(pygame.mouse.get_pos()):
                    end_game = False
                    game_over = False
                elif play_again_rect.collidepoint(pygame.mouse.get_pos()):
                    play_again = True
                    game_over = False
                    end_game = False

        # reset the screen
        screen.fill((0, 0, 0))

        # draw the title, buttons, and player image
        screen.blit(game_over_title, game_over_rect)
        screen.blit(play_again_text, play_again_rect)
        screen.blit(end_quit_text, end_quit_rect)
        screen.blit(dead_image, dead_rect)

        # update the screen
        pygame.display.flip()

    # fade out the music when finished the game
    music.fadeout(1000)

    # set event and player variables
    current_level = 11
    border = WIDTH
    camera.offset_float = 0
    player.velocity.y = 0
    player.position = pygame.math.Vector2(0, 680)
    player.rect.bottom = 680
    player.end_game = True
    player.right_key, player.left_key = False, False
    player.facing_left = False
    ended = False
    player.on_ground = True

    # hide the title and buttons
    end_text = title_font.render('', True, (255, 255, 255))
    end_rect = end_text.get_rect(center=(WIDTH / 2, 200))

    play_again_text = button_font.render('', True, (255, 255, 255))
    play_again_rect = play_again_text.get_rect(center=(0, 0))

    end_quit_text = button_font.render('', True, (255, 255, 255))
    end_quit_rect = end_quit_text.get_rect(center=(0, 0))

    # set player state for animation
    end_game_time = time
    player_state = "run_right"
    yay = pygame.mixer.Sound('audio/yay.wav')

    # end game loop
    while end_game:

        # delta time
        dt = clock.tick(60) * 0.001 * TARGET_FPS

        # update time variable for interval calculations
        time = pygame.time.get_ticks()

        #event loop
        for event in pygame.event.get():
            # quit game
            if event.type == pygame.QUIT:
                end_game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    end_game = False

            # update player image for animation
            if event.type == NEW_PLAYER_FRAME:
                player.update_frame(player_state, False, False, player_state)

            # check mouse clicks for buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                if end_quit_rect.collidepoint(pygame.mouse.get_pos()):
                    end_game = False
                elif play_again_rect.collidepoint(pygame.mouse.get_pos()):
                    play_again = True
                    end_game = False

        # reset screen
        screen.fill((0, 0, 0))

        # load empty level
        tile_rects1, spike_rects1 = tiles.draw(screen, levels[current_level * 2], 0, 0, 9, camera)
        tile_rects2, spike_rects2 = tiles.draw(screen, levels[current_level * 2 + 1], 1, 0, 9, camera)

        # combine rect lists
        tile_rects = tile_rects1 + tile_rects2
        spike_rects = spike_rects1 + spike_rects2

        # stop running after a certain time
        if time - end_game_time > 3150:
            player.right_key = False
            player_state = 'idle_right'
        else:
            player.right_key = True

        # display title after a certain time
        if time - end_game_time > 5000 and not ended:
            ended = True
            end_text = title_font.render('You escaped the dungeon!', True, (255, 255, 255))
            end_rect = end_text.get_rect(center=(WIDTH / 2, 200))
            yay.play()

        # display buttons after a certain time
        if time - end_game_time > 7000:
            play_again_text = button_font.render('play again', True, (255, 255, 255))
            play_again_rect = play_again_text.get_rect(center=(WIDTH / 2 - 200, 900))

            end_quit_text = button_font.render('quit', True, (255, 255, 255))
            end_quit_rect = end_quit_text.get_rect(center=(WIDTH / 2 + 200, 900))

        # update the player
        player.update(dt, tile_rects, spike_rects, border, camera, inventory, enemies.sprites(), health_bar, current_level)

        # update the camera offset
        camera.scroll()

        # draw the title and buttons
        screen.blit(end_text, end_rect)
        screen.blit(play_again_text, play_again_rect)
        screen.blit(end_quit_text, end_quit_rect)

        # draw the player
        player.draw(screen)

        # update the screen
        pygame.display.flip()

# run main()
if __name__ == "__main__":
    # plays again if play again button has been pressed
    while play_again:
        main()

    # exits the program
    pygame.quit()
    sys.exit()
