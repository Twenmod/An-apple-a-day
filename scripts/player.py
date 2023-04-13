import os
import pygame
from pygame.locals import *
from scripts.gameobject import *

class Player(gameObject):
    def __init__(self, sprite='Player.png', scale=(0.5,0.5), isKinematic=False, drag=0, speed = 1):
        print(sprite)
        super(Player, self).__init__(sprite, scale, isKinematic, drag)

        self.speed = speed
        self.drag = drag
        self.horizontalinput = 0
        self.verticalinput = 0

    def on_loop(self, deltaTime):
        super().on_loop(deltaTime)

        self.velocity_x = self.horizontalinput * self.speed
        self.velocity_y = self.verticalinput * self.speed
    def on_event(self, event):
        super().on_event(event)
        
        self.horizontalinput = 0
        self.verticalinput = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.horizontalinput = -1
        if keys[pygame.K_d]:
            self.horizontalinput = 1
        if keys[pygame.K_w]:
            self.verticalinput = 1
        if keys[pygame.K_s]:
            self.verticalinput = -1
        pass
