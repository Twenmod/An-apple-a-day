import os
import pygame
from pygame.locals import *
from scripts.gameobject import *
from scripts.tree import * 
from scripts.projectile import *

class Player(gameObject):
    def __init__(self,camgroup,enemylist, sprite='Player.png', scale=(0.5,0.5), isKinematic=False, drag=0, speed = 1, maxhealth=10):
        super(Player, self).__init__(sprite, scale, isKinematic, drag)
        self.cameragroup = camgroup
        self.speed = speed
        self.drag = drag
        self.horizontalinput = 0
        self.verticalinput = 0
        self.maxhealth = maxhealth
        self.health = self.maxhealth
        self.enemylist = enemylist

    def on_loop(self, deltaTime):
        super().on_loop(deltaTime)

        self.velocity_x = self.horizontalinput * self.speed
        self.velocity_y = self.verticalinput * self.speed

        mouse = pygame.mouse.get_pressed()
        mousepos = pygame.mouse.get_pos()
        if mouse[0]:
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
        relativemousepositionx = self.rect.centerx - mouseposition[0]
        relativemousepositiony = self.rect.centery - mouseposition[1]
        mousedir = pygame.math.Vector2(relativemousepositionx,relativemousepositiony)
        mousedir.normalize()
        if attacktype == "normalapple":
            proj = projectile(self,self.cameragroup,self.enemylist,'Box.png',(0.1,0.1),0,(self.position.x,self.position.y),mousedir,True,2,1)
            self.cameragroup.add(proj)
            pass
        elif attacktype == "SWITCHSTATEMENT":
            pass
        pass

    def plant_tree(self, type):
        treetypes = [tree((4,4),1,"tree")]
        spawned = treetypes[type]
        spawned.position = self.position
        spawned.player = self
        self.cameragroup.add(spawned)
