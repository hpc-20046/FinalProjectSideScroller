import pygame
import sys 
import os
import json
from settings import *
from player import Player
from tilemap import TileMap
from camera import *


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

    current_level = 1

    player = Player(100, 0, 3, WIDTH * 2)

    camera = Camera(player)
    #follow = Follow(camera, player)
    #border = Border(camera, player)
    #auto = Auto(camera, player)
    #camera.setmethod(follow)

    NEW_PLAYER_FRAME = pygame.USEREVENT
    pygame.time.set_timer(NEW_PLAYER_FRAME, 150)

    running = True
    while running:

        # delta time - so player speed will look the same no matter the frame rate
        dt = clock.tick(60) * 0.001 * TARGET_FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_LEFT:
                    player.turn(True)
                    player.LEFT_KEY, player.FACING_LEFT = True, True
                elif event.key == pygame.K_RIGHT:
                    player.turn(False)
                    player.RIGHT_KEY, player.FACING_LEFT = True, False
                elif event.key == pygame.K_SPACE:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.LEFT_KEY = False
                elif event.key == pygame.K_RIGHT:
                    player.RIGHT_KEY = False
                elif event.key == pygame.K_SPACE:
                    if player.is_jumping:
                        player.velocity.y *= 0.25
                        player.is_jumping = False

            if event.type == NEW_PLAYER_FRAME:
                if not player.FACING_LEFT:
                    player.update_frame("idle_right")
                elif player.FACING_LEFT:
                    player.update_frame("idle_left")
                else:
                    player.update_frame("idle_right")

        screen.fill((0, 0, 0))

        tile_rects1, spike_rects1 = tiles.draw(screen, levels[current_level - 1], 0, 0, backgrounds[current_level - 1], 9, camera)
        tile_rects2, spike_rects2 = tiles.draw(screen, levels[current_level], 1, 0, backgrounds[current_level - 1], 9, camera)

        tile_rects = tile_rects1 + tile_rects2
        spike_rects = spike_rects1 + spike_rects2
        
        player.update(dt, tile_rects, spike_rects, WIDTH * 2, camera)
        camera.scroll()
        
        player.draw(screen, camera)
        
        pygame.display.flip()


if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()