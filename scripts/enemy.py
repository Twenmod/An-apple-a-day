import os
import pygame
from pygame.locals import *
from scripts.gameobject import *

class enemy(gameObject):

    attackspeed = 1
    _attackcool = 0
    walkspeed = 1
    target = None 
    def __init__(self, sprite='Player.png', scale=(0.5,0.5), startposition=(0,0), walkspeed=1, player=None, attackspeed = 1):
        super().__init__(sprite, scale, True, 0, startposition)
        self.walkspeed = walkspeed
        self.target = player
        self.attackspeed = attackspeed


    def on_loop(self, deltaTime):
        super().on_loop(deltaTime)

        #move to player
        playerdir = self.target.position - self.position
        if (playerdir.magnitude() > 0):
            playerdir = playerdir.normalize()
        self.position += playerdir * deltaTime * self.walkspeed

        #attack
        self._attackcool -= deltaTime
        if (self._attackcool <= 0):
            self._attackcool = self.attackspeed
            self.attack()
    def attack(self):
        
        pass