import os
import pygame
from pygame.locals import *
from scripts.gameobject import *
from scripts.tree import * 
from scripts.projectile import *


class Player(gameObject):

    normalApples = 10
    poisonApples = 0

    def __init__(self,camgroup,enemylist, sprite='Player.png', scale=(0.5,0.5), isKinematic=False, drag=0, speed = 1, maxhealth=10, baseattackdamage = 1, baseattackvelocity = 100,baseattackdelay = 1, map=None):
        super(Player, self).__init__(sprite, scale, isKinematic, drag)
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

    def on_loop(self, deltaTime):
        super().on_loop(deltaTime)

        self.velocity_x = self.horizontalinput * self.speed
        self.velocity_y = self.verticalinput * self.speed

        mouse = pygame.mouse.get_pressed()
        mousepos = pygame.mouse.get_pos()
        self.attackdelay -= deltaTime 
        if mouse[0]:
            if self.attackdelay <= 0:
                self.attack("normalapple", mousepos)

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
        if keys[pygame.K_f]:
            self.plant_tree(0)

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


    def plant_tree(self, type):
        plant_position = pygame.math.Vector2(self.rect.center)
        plant_position.y += self.rect.height/2
        plant_position.x -= self.rect.width/2
        plant_position.x = round(plant_position.x/50)*50
        plant_position.y = round(plant_position.y/50)*50


        #find closest rect
        closestdist = 10^99
        closesttile = None
        for tile in self.worldmap.plantabletiles:
            dist = pygame.math.Vector2.distance_to(plant_position,tile.rect.center)
            if dist < closestdist:
                closestdist = dist
                closesttile = tile
        if (closesttile != None):
            if (closesttile.rect.collidepoint(plant_position)): # test if on dirt
                treetypes = [tree((4,4),1,"tree")]
                spawned = treetypes[type]
                spawned.position.x = round(((self.position.x - self.rect.width/2)/50))*50
                spawned.position.y = round(((self.position.y - self.rect.height/2)/50))*50
                spawned.player = self
                self.cameragroup.add(spawned)
