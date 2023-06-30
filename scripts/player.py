import os
import pygame
from pygame.locals import *
from scripts.gameobject import *
from scripts.tree import * 
from scripts.projectile import *


class Player(gameObject):

    normalApples = 20
    poisonApples = 0
    seeds = [10]
    treePlantingCooldown = 1
    score = 0
    walkanimspeed = 0.15
    slidedelay = 0
    currentslide = 0

    def __init__(self,camgroup, tree_list, enemylist, sprite='Player.png',walkanim=['playerstep0.png','playerstep1.png'], scale=(0.5,0.5), isKinematic=False, drag=0, speed = 1, maxhealth=10, baseattackdamage = 1, baseattackvelocity = 100,baseattackdelay = 1, map=None):
        super(Player, self).__init__(sprite, scale, isKinematic, drag,(50*22,50*18))
        self.cameragroup = camgroup
        self.speed = speed
        self.drag = drag
        self.horizontalinput = 0
        self.verticalinput = 0
        self.maxhealth = maxhealth
        self.health = self.maxhealth
        self.enemylist = enemylist
        self.baseattackvelocity = baseattackvelocity
        self.baseattackdamage = baseattackdamage
        self.baseattackvelocity = baseattackvelocity
        self.baseattackdelay = baseattackdelay
        self.attackdelay = 0
        self.worldmap = map
        self.tree_list = tree_list
        self.walkanimsprites = walkanim
        self.sprite = sprite
        self.scale = scale

    def on_loop(self, deltaTime):
        super().on_loop(deltaTime)

        self.treePlantingCooldown -= deltaTime

        self.velocity_x = self.horizontalinput * self.speed
        self.velocity_y = self.verticalinput * self.speed

        mouse = pygame.mouse.get_pressed()
        mousepos = pygame.mouse.get_pos()
        self.attackdelay -= deltaTime 
        if mouse[0]:
            if self.attackdelay <= 0:
                self.attack("normalapple", mousepos)

        # walk animation
        if (pygame.Vector2(self.horizontalinput,self.verticalinput).magnitude() > 0):
            self.slidedelay -= deltaTime
            if self.currentslide >= (len(self.walkanimsprites)):
                self.currentslide = 0
            elif (self.slidedelay <= 0):
                self.images = []
                img = pygame.image.load(os.path.join('images/', self.walkanimsprites[self.currentslide])).convert_alpha()
                img.set_colorkey(255)
                imgwidth = img.get_width()
                imgheight = img.get_height()
                imgsize = (imgwidth* self.scale[0], imgheight* self.scale[1]) 
                img = pygame.transform.scale(img, imgsize)
                self.images.append(img)
                self.image = self.images[0]
                self.currentslide += 1
                self.slidedelay = self.walkanimspeed
        else:
            self.images = []
            img = pygame.image.load(os.path.join('images/', self.sprite)).convert_alpha()
            img.set_colorkey(255)
            imgwidth = img.get_width()
            imgheight = img.get_height()
            imgsize = (imgwidth* self.scale[0], imgheight* self.scale[1]) 
            img = pygame.transform.scale(img, imgsize)
            self.images.append(img)
            self.image = self.images[0]

    def on_event(self, event):
        super().on_event(event)
        
        self.horizontalinput = 0
        self.verticalinput = 0
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.horizontalinput = -1
        if keys[pygame.K_d]:
            self.horizontalinput = 1
        if keys[pygame.K_w]:
            self.verticalinput = 1
        if keys[pygame.K_s]:
            self.verticalinput = -1
        if keys[pygame.K_f] and self.treePlantingCooldown <= 0:
            self.plant_tree(0)
            self.treePlantingCooldown = 0.25
        if keys[pygame.K_g] and self.treePlantingCooldown <= 0:
            self.plant_tree(1)
            self.treePlantingCooldown = 0.25
        if keys[pygame.K_h] and self.treePlantingCooldown <= 0:
            self.plant_tree(2)
            self.treePlantingCooldown = 0.25

        pass

    def takedamage(self, damage):
        self.health -= damage
        if (self.health <= 0):
            self.kill()
            #DIE
    def attack(self, attacktype,mouseposition):
        relativemousepositionx = mouseposition[0] - pygame.display.get_surface().get_width()/2
        relativemousepositiony = mouseposition[1] - pygame.display.get_surface().get_height()/2
        mousedir = pygame.math.Vector2(relativemousepositionx,relativemousepositiony)
        mousedir = mousedir.normalize()
        if attacktype == "normalapple":
            if self.normalApples <= 0:
                pass
            else:
                self.normalApples -= 1
                self.attackdelay = self.baseattackdelay
                proj = projectile(self,self.cameragroup,self.enemylist,'NormalApple.png',(1,1),0,(self.rect.centerx,self.rect.centery),mousedir * 5 * self.baseattackvelocity,True,2,1)
                self.cameragroup.add(proj)
                pass
        elif attacktype == "SWITCHSTATEMENT":
            pass
        pass


    def plant_tree(self, typetospawn):
        plant_position = pygame.math.Vector2(self.rect.center)
        plant_position.y += self.rect.height/2
        plant_position.x -= self.rect.width/2
        plant_position.x = (round(plant_position.x/50)*50)+25
        plant_position.y = (round(plant_position.y/50)*50)-25


        #find closest rect
        closestdist = 10^99
        closesttile = None
        for tile in self.worldmap.plantabletiles:
            dist = pygame.math.Vector2.distance_to(plant_position,tile.rect.center)
            if dist < closestdist:
                closestdist = dist
                closesttile = tile
        if (closesttile != None):
            if (closesttile.rect.collidepoint(plant_position) and closesttile.plantable): # test if on dirt
                if (self.seeds[0] > 0):
                    if (typetospawn == 1 and self.seeds[0] < 10): return # return if not enough for MEGATREE
                    if (typetospawn == 2 and self.seeds[0] < 5): return # return if not enough for hearttree
                    if (typetospawn == 0): self.seeds[0] -= 1
                    if (typetospawn == 1): self.seeds[0] -= 10
                    if (typetospawn == 2): self.seeds[0] -= 5

                    treetypes = [tree(self.cameragroup,(4,4),5.5,"tree",(0,0),self,closesttile),tree(self.cameragroup,(8,8),2,"megatree",(0,0),self,closesttile),tree(self.cameragroup,(4,4),5.5,"hearttree",(0,0),self,closesttile)]
                    spawned = treetypes[typetospawn]
                    spawned.position.x = round(((self.position.x - self.rect.width/2)/50))*50
                    spawned.position.y = round(((self.position.y - self.rect.height/2)/50))*50
                    if (typetospawn == 1):
                        spawned.position.x -= 90
                        spawned.position.y -= 150
                    spawned.player = self
                    self.cameragroup.add(spawned)
                    self.tree_list.add(spawned)
