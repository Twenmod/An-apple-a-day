import os
import pygame
from pygame.locals import *
import main
from scripts.gameobject import *

class projectile (gameObject):

    lifeTime = 1
    damage  = 1

    def __init__(self, object_list, sprite='Box.png', scale=(0.1,0.1), drag=0, startposition=(0,0), startvelocity=(0,0), tag="enemy",lifeTime=1, damage = 1):
        super().__init__(sprite, scale, False, drag, startposition)
        self.velocity_x = startvelocity.x
        self.velocity_y = startvelocity.y
        self.lifeTime = lifeTime
        self.damage = damage
        self.object_list = object_list

    def on_loop(self, deltaTime):
        super().on_loop(deltaTime)
        self.lifeTime -= deltaTime
        if (self.lifeTime <= 0):
            self.die()
    def die(self):
        self.object_list.remove(self)
        pass
