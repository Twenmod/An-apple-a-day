import os
import pygame
from pygame.locals import *

class gameObject(pygame.sprite.Sprite):
    velocity_x = 0
    velocity_y = 0
    isKinematic = False
    drag = 0
    gravity = 0
    position = [0,0]
    
    def __init__(self, sprite = 'Player.png', scale = (0.5, 0.5),isKinematic = False, drag = 0, gravity = 0.1, startposition = [0,0]):

        pygame.sprite.Sprite.__init__(self)
        self.images = []

        img = pygame.image.load(os.path.join('images', sprite)).convert()
        img.convert_alpha()
        img.set_colorkey(255)
        imgwidth = img.get_width()
        imgheight = img.get_height()
        imgsize = (imgwidth* scale[0], imgheight* scale[1]) 
        img = pygame.transform.scale(img, imgsize)
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.position = startposition
        pass
    def on_loop(self):

        if not (self.isKinematic):
            #Gravity
            self.velocity_y -= self.gravity

            #Add velocity
            self.position[0] += self.velocity_x
            self.position[1] -= self.velocity_y

            #Drag
            self.velocity_x /= (1+self.drag)
            self.velocity_y /= (1+self.drag)

        #Set sprite to position
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        
        pass
    def on_event(self, event):
        pass