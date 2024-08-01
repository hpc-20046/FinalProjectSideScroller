import pygame
from settings import *
import os
import json


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

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



    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill((0, 0, 0))

        for x in range(0, int(WIDTH/cell_width)+1):
            for y in range(0, int(HEIGHT/cell_height)+1):
                if levels[current_level - 1]["level"][x][y] == 0:
                    continue
                else:
                    screen.blit(tile_surfaces[levels[current_level - 1]["level"][x][y] - 1], tile_surfaces[levels[current_level - 1]["level"][x][y] - 1].get_rect(topleft=(cell_width * x, cell_height * y)))

        pygame.display.flip()



if __name__ == "__main__":
    main()
    pygame.quit()
