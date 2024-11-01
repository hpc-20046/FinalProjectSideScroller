import pygame
from settings import *
import os
from enemy import Enemy

# loads the tiles from the directory and converts them to pygame images
def load_tiles(path):
    tile_surfaces = []
    tile_list = os.scandir(path)
    with tile_list as tiles:
        for tile in tiles:
            tile_surfaces.append(pygame.transform.scale(pygame.image.load(tile.path), (CELL_WIDTH, CELL_HEIGHT)))
    total_tiles = len(tile_surfaces)
    return tile_surfaces, total_tiles

# spawns a group of enemies of different types
def spawn_enemies(pos, etype):
    group = pygame.sprite.Group()
    # spawns an enemy of the type given at every position given
    for i in range(len(pos)):
        match etype[i]:
            case 1:
                group.add(Enemy(['enemies/TinyDungeon/skelet_idle_anim_f0.png',
                          'enemies/TinyDungeon/skelet_idle_anim_f1.png',
                          'enemies/TinyDungeon/skelet_idle_anim_f2.png',
                          'enemies/TinyDungeon/skelet_idle_anim_f3.png'], ['enemies/TinyDungeon/skelet_run_anim_f0.png',
                                                                           'enemies/TinyDungeon/skelet_run_anim_f1.png',
                                                                           'enemies/TinyDungeon/skelet_run_anim_f2.png',
                                                                           'enemies/TinyDungeon/skelet_run_anim_f3.png'], pos[i], 3, 5, 5, etype[i]))
            case 2:
                group.add(Enemy([
                    'enemies/TinyDungeon/goblin_idle_anim_f0.png',
                    'enemies/TinyDungeon/goblin_idle_anim_f1.png',
                    'enemies/TinyDungeon/goblin_idle_anim_f2.png',
                    'enemies/TinyDungeon/goblin_idle_anim_f3.png',
                ], [
                    'enemies/TinyDungeon/goblin_run_anim_f0.png',
                    'enemies/TinyDungeon/goblin_run_anim_f1.png',
                    'enemies/TinyDungeon/goblin_run_anim_f2.png',
                    'enemies/TinyDungeon/goblin_run_anim_f3.png',
                ], pos[i], 3, 7, 5, etype[i]))
            case 3:
                group.add(Enemy([
                    'enemies/TinyDungeon/ogre_idle_anim_f0.png',
                    'enemies/TinyDungeon/ogre_idle_anim_f1.png',
                    'enemies/TinyDungeon/ogre_idle_anim_f2.png',
                    'enemies/TinyDungeon/ogre_idle_anim_f3.png'
                ], [
                    'enemies/TinyDungeon/ogre_run_anim_f0.png',
                    'enemies/TinyDungeon/ogre_run_anim_f1.png',
                    'enemies/TinyDungeon/ogre_run_anim_f2.png',
                    'enemies/TinyDungeon/ogre_run_anim_f3.png'
                ], pos[i], 3, 10, 10, etype[i]))

            case _:
                group.add(Enemy(['enemies/TinyDungeon/skelet_idle_anim_f0.png',
                                 'enemies/TinyDungeon/skelet_idle_anim_f1.png',
                                 'enemies/TinyDungeon/skelet_idle_anim_f2.png',
                                 'enemies/TinyDungeon/skelet_idle_anim_f3.png'], ['enemies/TinyDungeon/skelet_run_anim_f0.png',
                                                                                  'enemies/TinyDungeon/skelet_run_anim_f1.png',
                                                                                  'enemies/TinyDungeon/skelet_run_anim_f2.png',
                                                                                  'enemies/TinyDungeon/skelet_run_anim_f3.png'],
                                pos[i], 3, 5, 5, etype[i]))
    return group

# handles the map visuals
class TileMap:
    def __init__(self, path):
        # load the tiles
        self.tiles, self.total_tiles = load_tiles(path)

    def draw(self, display, level, gridx, gridy, spike, camera):
        tile_rects = []
        spike_rects = []
        # change where the level is drawn based on its world grid position
        grid_factor_x = gridx * WIDTH
        grid_factor_y = gridy * HEIGHT
        # loops through every cell on the grid
        for x in range(0, int(WIDTH / CELL_WIDTH) + 1):
            for y in range(0, int(HEIGHT / CELL_HEIGHT) + 1):
                # if the cell is empty space, don't draw
                if level["level"][x][y] == 0:
                    continue

                # if the cell is inside a wall or floor, draw but without a rect
                elif level["level"][x][y] == self.total_tiles:
                    display.blit(self.tiles[level["level"][x][y] - 1], self.tiles[level["level"][x][y] - 1]
                                 .get_rect(topleft=((CELL_WIDTH * x + grid_factor_x) - camera.offset_float, (CELL_HEIGHT * y + grid_factor_y))))

                # if the cell is a spike, draw and append the rect to a seperate list
                elif level["level"][x][y] == spike:
                    rect = self.tiles[level["level"][x][y] - 1].get_rect(topleft=((CELL_WIDTH * x + grid_factor_x)
                                                                                  - camera.offset_float, (CELL_HEIGHT * y + grid_factor_y)))
                    spike_rects.append(rect)
                    display.blit(self.tiles[level["level"][x][y] - 1], rect)
                # draw and append rect to list
                else:
                    rect = self.tiles[level["level"][x][y] - 1].get_rect(topleft=((CELL_WIDTH * x + grid_factor_x)
                                                                                  - camera.offset_float, (CELL_HEIGHT * y + grid_factor_y)))
                    tile_rects.append(rect)
                    display.blit(self.tiles[level["level"][x][y] - 1], rect)

        return tile_rects, spike_rects


