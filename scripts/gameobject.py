import os
import pygame
from pygame.locals import *

class gameObject(pygame.sprite.Sprite):
    velocity_x = 0
    velocity_y = 0
    isKinematic = False
    drag = 0
    position = pygame.math.Vector2(0,0)
    
    def __init__(self, sprite = 'Player.png', scale = (0.5, 0.5),isKinematic = False, drag = 0, startposition = (0,0)):
        pygame.sprite.Sprite.__init__(self)
        self.images = []

        img = pygame.image.load(os.path.join('images', sprite)).convert_alpha()
        img.set_colorkey(255)
        imgwidth = img.get_width()
        imgheight = img.get_height()
        imgsize = (imgwidth* scale[0], imgheight* scale[1]) 
        img = pygame.transform.scale(img, imgsize)
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.position = pygame.math.Vector2(startposition)
        pass

    def on_loop(self, deltaTime):
        if not (self.isKinematic):

            #Add velocity
            self.position.x += self.velocity_x*deltaTime
            self.position.y -= self.velocity_y*deltaTime

            #Drag
            self.velocity_x /= (1+self.drag)
            self.velocity_y /= (1+self.drag)

        #Set sprite to position
        self.rect.x = self.position.x
        self.rect.y = self.position.y
        
        pass
    def on_event(self, event):
        pass