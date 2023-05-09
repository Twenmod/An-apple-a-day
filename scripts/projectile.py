import os
import pygame
from pygame.locals import *
from scripts.gameobject import *

class projectile (gameObject):
    def __init__(self, sprite='Box.png', scale=(0.1,0.1), drag=0, startposition=(0,0), startvelocity=(0,0), tag="enemy"):
        super().__init__(sprite, scale, False, drag, startposition)
        self.velocity_x = startvelocity.x
        self.velocity_y = startvelocity.y

    def on_loop(self, deltaTime):
        super().on_loop(deltaTime)
    def break():
        pass
