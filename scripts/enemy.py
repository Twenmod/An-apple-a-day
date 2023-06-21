import os
import pygame
from pygame.locals import *
from scripts.gameobject import *
from scripts.projectile import *
from scripts.droppeditem import *

class enemy(gameObject):

    attackspeed = 1
    _attackcool = 0
    attackVelocity = 1
    attackDamage = 1
    walkspeed = 1
    target = None 

    def __init__(self, object_list=None, tree_list = None, sprite='Player.png', scale=(0.5,0.5), startposition=(0,0), walkspeed=1, player=None, attackspeed = 1, attackVelocity = 1, attackDamage = 1, maxhealth = 10):
        super().__init__(sprite, scale, True, 0, startposition)
        self.walkspeed = walkspeed
        self.target = player
        self.attackspeed = attackspeed
        self.attackVelocity = attackVelocity
        self.attackDamage = attackDamage
        self.object_list = object_list
        self.health = maxhealth
        self.tree_list = tree_list

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

        proj = projectile(self.target,self.object_list, self.tree_list, 'Syringe.png', (1.6,1.6), 0, (self.rect.centerx,self.rect.centery), playerdir*self.attackVelocity, False, 5, 1)
        self.object_list.add(proj)
        pass
    def takedamage(self, damage):
        self.health -= damage
        if (self.health <= 0):
            #Drop seeds
            amountofitems = random.randrange(0,5)
            while(amountofitems > 0):
                drops = [None,None,None,droppeditem(self.target,'seeds.png',(2.5,2.5),False,5,(self.rect.centerx,self.rect.centery),(random.randrange(-200,200),random.randrange(-200,200)),"normalSeeds")]
                amountofitems-=1 
                drop = drops[random.randrange(0,len(drops),1)]
                if (drop != None):
                    self.object_list.add(drop)
            self.target.score += 15
            self.kill()
            #DIE