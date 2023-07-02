import pygame
from pygame.locals import *
from scripts.gameobject import *
import random

class mainmenuparticle(gameObject):
    def __init__(self, sprite='Player.png', scale=..., isKinematic=False, drag=0,gravity=9.81, startposition=..., startvelocity=(0,0), lifeTime=1):
        super().__init__(sprite, scale, isKinematic, drag, startposition)
        self.gravity = gravity
        self.velocity_x = startvelocity[0]
        self.velocity_y = startvelocity[1]
        self.lifeTime = lifeTime
    def on_loop(self, deltaTime):
        super().on_loop(deltaTime)
        self.velocity_y -= deltaTime*self.gravity
        self.lifeTime -= deltaTime
        if (self.lifeTime <= 0):
            self.kill()