import os
import pygame
from pygame.locals import *
from scripts.gameobject import *
from scripts.particlesystem import *

class projectile (gameObject):

    lifeTime = 1
    damage  = 1

    currentRot = 0

    def __init__(self, player, object_list, enemylist, sprite='Box.png', scale=(0.1,0.1), drag=0, startposition=(0,0), startvelocity=(0,0), playershot=False,lifeTime=1, damage = 1, rotationSpeed = -350):
        super().__init__(sprite, scale, False, drag, startposition)
        self.velocity_x = startvelocity.x
        self.velocity_y = -startvelocity.y
        self.lifeTime = lifeTime
        self.damage = damage
        self.object_list = object_list
        self.player = player
        self.playershot = playershot
        self.enemylist = enemylist
        self.rotationSpeed = rotationSpeed
        self.sprite = sprite
        self.scale = scale

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
            if pygame.sprite.spritecollide(self,self.enemylist,False):
                hit = pygame.sprite.spritecollideany(self,self.enemylist)
                hit.takedamage(self.damage)
                self.die()
        else:
            if (pygame.sprite.spritecollideany(self,self.enemylist)):
                hit = pygame.sprite.spritecollideany(self,self.enemylist)
                hit.takedamage(self.damage)
                self.die()
    
        #rotate
        self.currentRot += deltaTime*self.rotationSpeed

        self.images = []

        img = pygame.image.load(os.path.join('images', self.sprite)).convert_alpha()
        self.mask = pygame.mask.from_surface(img)
        img.set_colorkey(255)
        imgwidth = img.get_width()
        imgheight = img.get_height()
        imgsize = (imgwidth* self.scale[0], imgheight* self.scale[1]) 
        img = pygame.transform.scale(img, imgsize)
        img = pygame.transform.rotate(img, self.currentRot)
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=self.rect.center)



    def die(self):
        if (self.playershot):
            part = particle((1,1),False,0,(self.rect.centerx, self.rect.centery),["applehit/stage0.png","applehit/stage1.png","applehit/stage2.png","applehit/stage3.png"],0.025)
        else:
            part = particle((1,1),False,0,(self.rect.centerx, self.rect.centery),["syringehit/stage0.png","syringehit/stage1.png","syringehit/stage2.png","syringehit/stage3.png"],0.025)
        self.object_list.add(part)
        self.kill()
        pass
