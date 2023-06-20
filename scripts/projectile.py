import os
import pygame
from pygame.locals import *
from scripts.gameobject import *
from scripts.particlesystem import *

class projectile (gameObject):

    lifeTime = 1
    damage  = 1

    def __init__(self, player, object_list, enemylist, sprite='Box.png', scale=(0.1,0.1), drag=0, startposition=(0,0), startvelocity=(0,0), playershot=False,lifeTime=1, damage = 1):
        super().__init__(sprite, scale, False, drag, startposition)
        self.velocity_x = startvelocity.x
        self.velocity_y = -startvelocity.y
        self.lifeTime = lifeTime
        self.damage = damage
        self.object_list = object_list
        self.player = player
        self.playershot = playershot
        self.enemylist = enemylist

    def on_loop(self, deltaTime):
        super().on_loop(deltaTime)
        self.lifeTime -= deltaTime
        if (self.lifeTime <= 0):
            self.die()

        #collision
        # check with player
        if not (self.playershot):
            if (self.rect.colliderect(self.player.rect)):
                self.player.takedamage(self.damage)
                self.die()
            if (pygame.sprite.spritecollideany(self,self.enemylist)):
                hit = pygame.sprite.spritecollideany(self,self.enemylist)
                hit.takedamage(self.damage)
                self.die()
        else:
            if (pygame.sprite.spritecollideany(self,self.enemylist)):
                hit = pygame.sprite.spritecollideany(self,self.enemylist)
                hit.takedamage(self.damage)
                self.die()

            

    def die(self):
        #particlesystem("Box.png",self.object_list,(1,10),0.5,-0.1,(1,1),(1,10),5,(self.rect.centerx, self.rect.centery))
        self.kill()
        pass
