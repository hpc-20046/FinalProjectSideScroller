import pygame
from settings import *
import os
from enemy import Enemy


def load_tiles(path):
    tile_surfaces = []
    tile_list = os.scandir(path)
    with tile_list as tiles:
        for tile in tiles:
            tile_surfaces.append(pygame.transform.scale(pygame.image.load(tile.path), (cell_width, cell_height)))
    total_tiles = len(tile_surfaces)
    return tile_surfaces, total_tiles

def spawn_enemies(pos, etype):
    group = pygame.sprite.Group()
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


class TileMap:
    def __init__(self, path):
        self.tiles, self.total_tiles = load_tiles(path)

    def draw(self, display, level, gridx, gridy, spike, camera):
        tile_rects = []
        spike_rects = []
        grid_factor_x = gridx * WIDTH
        grid_factor_y = gridy * HEIGHT
        for x in range(0, int(WIDTH/cell_width)+1):
            for y in range(0, int(HEIGHT/cell_height)+1):
                if level["level"][x][y] == 0:
                    continue
                
                elif level["level"][x][y] == self.total_tiles:
                    display.blit(self.tiles[level["level"][x][y] - 1], self.tiles[level["level"][x][y] - 1].get_rect(topleft=((cell_width * x + grid_factor_x) - camera.offset_float, (cell_height * y + grid_factor_y))))
                    
                elif level["level"][x][y] == spike:
                    rect = self.tiles[level["level"][x][y] - 1].get_rect(topleft=((cell_width * x + grid_factor_x) - camera.offset_float, (cell_height * y + grid_factor_y)))
                    spike_rects.append(rect)
                    display.blit(self.tiles[level["level"][x][y] - 1], rect)

                else:
                    rect = self.tiles[level["level"][x][y] - 1].get_rect(topleft=((cell_width * x + grid_factor_x) - camera.offset_float, (cell_height * y + grid_factor_y)))
                    tile_rects.append(rect)
                    display.blit(self.tiles[level["level"][x][y] - 1], rect)

        return tile_rects, spike_rects


