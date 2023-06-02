import os
import pygame
from pygame.locals import *
from scripts.gameobject import *
from scripts.projectile import *

class enemy(gameObject):

    attackspeed = 1
    _attackcool = 0
    attackVelocity = 1
    attackDamage = 1
    walkspeed = 1
    target = None 
    def __init__(self, object_list=None, sprite='Player.png', scale=(0.5,0.5), startposition=(0,0), walkspeed=1, player=None, attackspeed = 1, attackVelocity = 1, attackDamage = 1):
        super().__init__(sprite, scale, True, 0, startposition)
        self.walkspeed = walkspeed
        self.target = player
        self.attackspeed = attackspeed
        self.attackVelocity = attackVelocity
        self.attackDamage = attackDamage
        self.object_list = object_list

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

        playerdir = self.target.position - self.position
        if (playerdir.magnitude() > 0):
            playerdir = playerdir.normalize()

        proj = projectile(self.target,self.object_list, None, 'Box.png', (0.1,0.1), 0, (self.rect.centerx,self.rect.centery), playerdir*self.attackVelocity, False, 5, 1)
        self.object_list.add(proj)
        pass
    def takedamage(self, damage):
        self.health -= damage
        if (self.health <= 0):
            self.kill()
            #DIE