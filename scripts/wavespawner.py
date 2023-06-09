import pygame
from pygame.locals import *
from scripts.enemy import *
from math import *
from random import *

class wave():
    def __init__(self, object_list, enemies = [None], amountofenemies = (2,5), spawnrange = 500):
        self.enemies = enemies
        self.amountofenemies = amountofenemies
        self.spawnrange = spawnrange
        self.object_list = object_list
        self.startwave()
    def startwave(self):
        amount = randrange(self.amountofenemies[0],self.amountofenemies[1],1)
        while amount > 0:
            amount-=1
            self.spawnenemy(self.enemies[randrange(0,len(self.enemies),1)])

        pass
    def spawnenemy(self, enemy):
        #get angle
        angle =  randrange(0,360,1)
        #get position
        spawnx = self.spawnrange * sin(angle)
        spawny = self.spawnrange * cos(angle)

        enemy.position.x = spawnx
        enemy.position.y = spawny
        self.object_list.add(enemy)
