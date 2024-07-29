import pygame
from settings import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                

    for x in range(0, int(WIDTH/cell_width)+1):
        for y in range(0, int(HEIGHT/cell_height)+1):
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(cell_width * x, cell_height * y, cell_width, cell_height), width=1)

    pygame.display.flip()

pygame.quit()
