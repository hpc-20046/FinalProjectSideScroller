import pygame
from settings import *
import os
import json
import math


# pygame initialisation 
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

tile_num = 0

# dynamically turn all images in a directory, turn them into surfaces, and add them to a list.
tile_surfaces = []
tile_list = os.scandir('dungeon/')
with tile_list as tiles:
    for tile in tiles:
        tile_surfaces.append(pygame.transform.scale(pygame.image.load(tile.path), (cell_width, cell_height)))
total_tiles = len(tile_surfaces)

# open level file to be edited
file = "levels/level1.json"

try:
    with open(file, 'r') as openfile:
        level = json.load(openfile)
except FileNotFoundError:
    open(file, 'x')
    temp = [[]]
    for x in range(0, int(WIDTH/cell_width)+1):
        for y in range(0, int(HEIGHT/cell_height)+1):
            temp[x].append(0)
        temp.append([])
    temp.pop(-1)
    level = {"level": temp}

# Game loop
running = True
while running:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_r:
                os.system("python FinalProjectSideScroller.py")
        if pygame.mouse.get_pressed()[0]:
            try:
                print(event.pos)
                pos = pygame.mouse.get_pos()
                cellx = math.floor(pos[0] / cell_width)
                celly = math.floor(pos[1] / cell_height)
                level["level"][cellx][celly] = tile_num
            except AttributeError:
                pass
        if pygame.mouse.get_pressed()[2]:
            try:
                print(event.pos)
                pos = pygame.mouse.get_pos()
                cellx = math.floor(pos[0] / cell_width)
                celly = math.floor(pos[1] / cell_height)
                level["level"][cellx][celly] = 0
            except AttributeError:
                pass
        if pygame.mouse.get_pressed()[1]:
            try:
                print(event.pos)
                pos = pygame.mouse.get_pos()
                cellx = math.floor(pos[0] / cell_width)
                celly = math.floor(pos[1] / cell_height)
                level["level"][cellx][celly] = total_tiles
            except AttributeError:
                pass
        if event.type == pygame.MOUSEWHEEL:
            tile_num += event.y
            pos = pygame.mouse.get_pos()
            cellx = math.floor(pos[0] / cell_width)
            celly = math.floor(pos[1] / cell_height)
            level["level"][cellx][celly] = tile_num
 
 

    screen.fill(pygame.Color('lightblue'))

    # draw grid with appropriate tiles.
    for x in range(0, int(WIDTH/cell_width)+1):
        for y in range(0, int(HEIGHT/cell_height)+1):
            if level["level"][x][y] == 0:
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(cell_width * x, cell_height * y, cell_width, cell_height), width=1)
            else:
                screen.blit(tile_surfaces[level["level"][x][y] - 1], tile_surfaces[level["level"][x][y] - 1].get_rect(topleft=(cell_width * x, cell_height * y)))

    pygame.display.flip()

# write level into file
with open(file, 'w') as outfile:
    json.dump(level, outfile)

pygame.quit()
