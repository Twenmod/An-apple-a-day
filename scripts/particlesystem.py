import pygame
from pygame.locals import *
from scripts.gameobject import *
import random

class particle(gameObject):

    slidedelay = 0
    currentslide = 0

    def __init__(self, scale=..., isKinematic=False, drag=0, startposition=..., slides=["tree/stage0.png","tree/stage1.png","tree/stage2.png"],slidespeed=1):
        super().__init__("particles/"+slides[0], scale, isKinematic, drag, (startposition[0]-15,startposition[1]-10))
        self.slides = slides
        self.slidespeed = slidespeed
        self.slidedelay = 0
        self.scale = scale

    def on_loop(self, deltaTime):
        super().on_loop(deltaTime)

        self.slidedelay -= deltaTime
        if self.currentslide >= (len(self.slides)):
            self.kill()
        elif (self.slidedelay <= 0):
            self.images = []
            img = pygame.image.load(os.path.join('images/particles/', self.slides[self.currentslide])).convert_alpha()
            img.set_colorkey(255)
            imgwidth = img.get_width()
            imgheight = img.get_height()
            imgsize = (imgwidth* self.scale[0], imgheight* self.scale[1]) 
            img = pygame.transform.scale(img, imgsize)
            self.images.append(img)
            self.image = self.images[0]
            self.currentslide += 1
            self.slidedelay = self.slidespeed


