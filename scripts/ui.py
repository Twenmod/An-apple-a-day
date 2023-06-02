import os
import pygame

class UI ():

    def __init__(self, display_surface):
        self.display_surface = display_surface
    def on_render(self):
        font = pygame.font.Font('fonts/LilitaOne-Regular.ttf', 32)
        text = font.render('FUCK', True, (0, 255, 0), (0, 0, 255))
        textRect = text.get_rect()
        textRect.center = (50, 50)
        self.display_surface.blit(text,textRect)

        