import pygame
from settings import *
import os


def load_tiles(path):
    tile_surfaces = []
    tile_list = os.scandir(path)
    with tile_list as tiles:
        for tile in tiles:
            tile_surfaces.append(pygame.transform.scale(pygame.image.load(tile.path), (cell_width, cell_height)))
    total_tiles = len(tile_surfaces)
    return tile_surfaces, total_tiles


class TileMap:
    def __init__(self, path, background):
        self.tiles, self.total_tiles = load_tiles(path)
        self.background_tiles, self.total_background_tiles = load_tiles(background)

    def draw(self, display, level, background, spike):
        tile_rects = []
        spike_rects = []
        for x in range(0, int(WIDTH/cell_width)+1):
            for y in range(0, int(HEIGHT/cell_height)+1):
                if level["level"][x][y] == 0:
                    #display.blit(self.background_tiles[background["level"][x][y] - 1], (cell_width * x, cell_height * y))
                    continue
                elif level["level"][x][y] == self.total_tiles:
                    display.blit(self.tiles[level["level"][x][y] - 1], self.tiles[level["level"][x][y] - 1]
                                 .get_rect(topleft=(cell_width * x, cell_height * y)))
                elif level["level"][x][y] == spike:
                    #display.blit(self.background_tiles[background["level"][x][y] - 1], (cell_width * x, cell_height * y))
                    rect = self.tiles[level["level"][x][y] - 1].get_rect(topleft=(cell_width * x, cell_height * y))
                    spike_rects.append(rect)
                    display.blit(self.tiles[level["level"][x][y] - 1], rect)
                else:
                    rect = self.tiles[level["level"][x][y] - 1].get_rect(topleft=(cell_width * x, cell_height * y))
                    tile_rects.append(rect)
                    display.blit(self.tiles[level["level"][x][y] - 1], rect)

        return tile_rects, spike_rects


