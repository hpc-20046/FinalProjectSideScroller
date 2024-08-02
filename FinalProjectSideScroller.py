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

    player_obj = Player(100, HEIGHT / 2, 3)
    player = pygame.sprite.Group()
    player.add(player_obj)
    player_x_change = 0
    is_jumping = False

    NEW_PLAYER_FRAME = pygame.USEREVENT
    pygame.time.set_timer(NEW_PLAYER_FRAME, 150)

    running = True
    while running:
        player_x_change = 0
        is_jumping = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x_change = -5
        if keys[pygame.K_RIGHT]:
            player_x_change = 5

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    is_jumping = True
            if event.type == NEW_PLAYER_FRAME:
                if player_x_change == 5:
                    player.sprites()[0].update_frame("idle_right")
                elif player_x_change == -5:
                    player.sprites()[0].update_frame("idle_left")
                else:
                    player.sprites()[0].update_frame("idle_right")



        screen.fill((0, 0, 0))

        tile_rects = []

        for x in range(0, int(WIDTH/cell_width)+1):
            for y in range(0, int(HEIGHT/cell_height)+1):
                if levels[current_level - 1]["level"][x][y] == 0:
                    continue
                else:
                    tile_rects.append(tile_surfaces[levels[current_level - 1]["level"][x][y] - 1]
                                      .get_rect(topleft=(cell_width * x, cell_height * y)))

                    screen.blit(tile_surfaces[levels[current_level - 1]["level"][x][y] - 1],
                                tile_surfaces[levels[current_level - 1]["level"][x][y] - 1]
                                .get_rect(topleft=(cell_width * x, cell_height * y)))

        player.update(player_x_change, is_jumping, tile_rects)
        player.draw(screen)
        pygame.display.flip()
        clock.tick(60)



if __name__ == "__main__":
    main()
    pygame.quit()
