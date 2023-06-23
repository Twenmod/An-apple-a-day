import os
import pygame
import random
from pygame.locals import *
from scripts.gameobject import *
from scripts.droppeditem import *
from scripts.particlesystem import *

class tree(gameObject):

    harvestdistance = 100

    scale=(1,1)
    player = None

    health = 5

    growthStages = [0,25,75,125,175,275]
    growthStage = 0
    growthSpeed = 1
    growth = 0
    stageSprites =["stage0.png", "stage1.png", "stage2.png","stage2-3.png", "stage3.png", "stage4.png"]
    type = "tree"

    def __init__(self, object_list, scale=(0.5,0.5), growthSpeed=1, type="tree", startpos=[0,0],player = None, tile=None):
        super(tree, self).__init__("tree/stage0.png", scale, True, 0,startpos)
        print("Treeinit")
        self.scale = scale
        self.growthSpeed = growthSpeed
        self.type = type
        self.player = player
        self.object_list = object_list
        tile.plantable = False
        self.tile = tile

    def on_loop(self, deltaTime):
        super().on_loop(deltaTime)
        #grow
        self.growth += deltaTime*self.growthSpeed*random.randrange(1,6,1)
        #print("Tree: "+ str(self.growthStage) + " | " + str(len(self.growthStages)-1))
        #Check growth
        if (self.growthStage < len(self.growthStages)-1):
            if (self.growth >= self.growthStages[self.growthStage+1]):
                self.growthStage += 1
                self.change_stage(self.growthStage)

        pass

    def change_stage(self,stage):

        self.images = []

        img = pygame.image.load(os.path.join('images/'+self.type+'/', self.stageSprites[stage])).convert_alpha()
        img.set_colorkey(255)
        imgwidth = img.get_width()
        imgheight = img.get_height()
        imgsize = (imgwidth* self.scale[0], imgheight* self.scale[1]) 
        img = pygame.transform.scale(img, imgsize)
        self.images.append(img)
        self.image = self.images[0]
        #self.rect = self.image.get_rect()

        pass

    def harvest(self):
        #drop apples
        if self.type == "tree":
            amountnormalApple = random.randrange(1,20)
            while amountnormalApple > 0:
                amountnormalApple-=1
                drop = droppeditem(self.player,"NormalApple.png",(1,1),False,5,(self.rect.centerx,self.rect.centery),(random.randrange(-200,200),random.randrange(-200,200)),"normalApple")
                self.object_list.add(drop)

        #return to last stage
        self.growth = self.growthStages[self.growthStage-1]
        self.growthStage -= 1
        self.change_stage(self.growthStage)

        #Particles
        part = particle((4,4),True,0,self.rect.topleft,["tree/harvest0.png","tree/harvest1.png","tree/harvest2.png","tree/harvest3.png"],0.15)
        self.object_list.add(part)

        pass

    def on_event(self, event):
        super().on_event(event)
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_e]):
            distance = pygame.math.Vector2.distance_to(pygame.math.Vector2(self.rect.centerx,self.rect.centery),self.player.position)
            print(distance)
            if (distance < self.harvestdistance):
                if (self.growthStage == len(self.growthStages)-1):
                    self.harvest()
        pass

    def takedamage(self, damage):
        if (self.growthStage == 0):
            self.tile.plantable = True
            self.kill()
        elif (self.growthStage==5):
            self.harvest()
        else:
            #return to last stage
            self.growth = self.growthStages[self.growthStage-1]
            self.growthStage -= 1
            self.change_stage(self.growthStage)

            #Particles
            part = particle((4,4),True,0,self.rect.topleft,["tree/harvest0.png","tree/harvest1.png","tree/harvest2.png","tree/harvest3.png"],0.15)
            self.object_list.add(part)



