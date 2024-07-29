import math

import pygame
from settings import *
import os
import json


def increment_cell_space():
    pos = pygame.mouse.get_pos()
    cellx = math.floor(pos[0] / cell_width)
    celly = math.floor(pos[1] / cell_height)

    if pygame.mouse.get_pressed()[2]:
        level["level"][cellx][celly] = 0
    else:
        level["level"][cellx][celly] += 1
        if level["level"][cellx][celly] > total_tiles:
            level["level"][cellx][celly] = 0


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

tile_surfaces = []
tile_list = os.scandir('dungeon/')
with tile_list as tiles:
    for tile in tiles:
        tile_surfaces.append(pygame.transform.scale(pygame.image.load(tile.path), (cell_width, cell_height)))
total_tiles = len(tile_surfaces)

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

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_r:
                os.system("python FinalProjectSideScroller.py")
        if event.type == pygame.MOUSEBUTTONDOWN:
            increment_cell_space()

    screen.fill(pygame.Color('lightblue'))

    for x in range(0, int(WIDTH/cell_width)+1):
        for y in range(0, int(HEIGHT/cell_height)+1):
            if level["level"][x][y] == 0:
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(cell_width * x, cell_height * y, cell_width, cell_height), width=1)
            else:
                screen.blit(tile_surfaces[level["level"][x][y] - 1], tile_surfaces[level["level"][x][y] - 1].get_rect(topleft=(cell_width * x, cell_height * y)))

    pygame.display.flip()

with open(file, 'w') as outfile:
    json.dump(level, outfile)

pygame.quit()
