import pygame
from pygame.locals import *
from scripts.enemy import *
from math import *
from random import *

class wave():
    def __init__(self, object_list, enemy_list, enemies = [None], amountofenemies = (2,5), spawnrange = 200):
        self.enemies = enemies
        self.amountofenemies = amountofenemies
        self.spawnrange = spawnrange
        self.object_list = object_list
        self.enemy_list = enemy_list
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

        enemy.position.x = spawnx+15*50
        enemy.position.y = spawny+15*50
        self.object_list.add(enemy)
        self.enemy_list.add(enemy)
