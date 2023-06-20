import pygame
from pygame.locals import *
from scripts.gameobject import *
import random

class particle(gameObject):
    def __init__(self, sprite='Player.png', scale=..., isKinematic=False, drag=0, startposition=..., lifetime=5, scalespeed=0):
        super().__init__(sprite, scale, isKinematic, drag, startposition)
        self.lifetime = lifetime
        self.scalespeed = scalespeed
        self.currentscale = [1,1]
        self.currentscale[0] = scale[0]
        self.currentscale[1] = scale[1]

    def on_loop(self, deltaTime):
        super().on_loop(deltaTime)
        self.lifetime -= deltaTime
        if self.lifetime <= 0:
            self.kill()
        self.currentscale[0] += self.scalespeed * deltaTime
        self.currentscale[1] += self.scalespeed * deltaTime
        self.scalesize(self.currentscale)
    
    def scalesize(self, scale):
        if (scale[0] <= 0): scale[0] = 0
        if (scale[1] <= 0): scale[1] = 0
        img = self.image
        imgwidth = img.get_width()
        imgheight = img.get_height()
        imgsize = (imgwidth* scale[0], imgheight* scale[1]) 
        self.image = pygame.transform.scale(img, imgsize)
        self.rect = self.image.get_rect()

class particlesystem():
    def __init__(self, sprite="Box.png", object_list=None, amount=(1,10), lifetime=0.1, scalespeed=-1, startscale=(1,1),speed=(1,10),drag=5,startposition=(0,0)) -> None:
        particleamount = random.randrange(amount[0],amount[1])
        while particleamount > 0:
            particleamount-=1
            inst = particle(sprite,startscale,False,drag,startposition,lifetime,scalespeed)
            object_list.add(inst)
            