import pygame
import os
import json
from settings import *
from player import Player


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    tile_surfaces = []
    tile_list = os.scandir('dungeon/')
    with tile_list as tiles:
        for tile in tiles:
            tile_surfaces.append(pygame.transform.scale(pygame.image.load(tile.path), (cell_width, cell_height)))
    total_tiles = len(tile_surfaces)

    levels = []
    level_list = os.scandir('levels/')
    with level_list as alevel:
        for level in alevel:
            with open(level.path, 'r') as openfile:
                levels.append(json.load(openfile))

    current_level = 1

    player = Player(100, HEIGHT / 2, 3)

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
                    player.LEFT_KEY, player.FACING_LEFT = True, True
                elif event.key == pygame.K_RIGHT:
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

        tile_rects = []

        for x in range(0, int(WIDTH/cell_width)+1):
            for y in range(0, int(HEIGHT/cell_height)+1):
                if levels[current_level - 1]["level"][x][y] == 0:
                    continue
                elif levels[current_level - 1]["level"][x][y] == total_tiles:
                    screen.blit(tile_surfaces[levels[current_level - 1]["level"][x][y] - 1],
                                tile_surfaces[levels[current_level - 1]["level"][x][y] - 1]
                                .get_rect(topleft=(cell_width * x, cell_height * y)))
                else:
                    tile_rect = tile_surfaces[levels[current_level - 1]["level"][x][y] - 1].get_rect(topleft=(cell_width * x, cell_height * y))
                    tile_rects.append(tile_rect)

                    screen.blit(tile_surfaces[levels[current_level - 1]["level"][x][y] - 1], tile_rect)

        player.update(dt, tile_rects)
        player.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()
    pygame.quit()
