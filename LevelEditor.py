import pygame
from settings import *
import os
import json

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

file = "level1.json"

try:
    with open(file, 'r') as openfile:
        level = json.load(openfile)
except e:
    
    

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





pygame.quit()