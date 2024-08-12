from gc import get_referents
from tkinter.tix import Tree
import pygame
from settings import *

class UserInterface:
    def __init__(self, pos_x, pos_y, width, height, image):
        self.state = "main_menu"
        self.font = pygame.font.Font('fonts/ARIAL.TTF', 40)
        self.position = pygame.math.Vector2(pos_x, pos_y)
        self.dimensions = pygame.math.Vector2(width, height)
        self.image = image
        self.title_rect = ""

    def draw(self, display):
        if self.state == 'main_menu':
            pygame.draw.rect(display, self.image, pygame.Rect(self.position.x - (self.dimensions.x / 2), self.position.y - (self.dimensions.y / 2 ), self.dimensions.x, self.dimensions.y))
            title_text = self.font.render("TITLE", True, (255, 255, 255))
            self.title_rect = title_text.get_rect(center=(WIDTH / 2, 500))

            display.blit(title_text, self.title_rect)
            
    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if self.title_rect.collidepoint(pygame.mouse.get_pos()):
                        print("chris is gay")
                                                                       