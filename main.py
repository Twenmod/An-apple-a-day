import os
import pygame
from pygame.locals import *
from scripts.gameobject import *
from scripts.player import *
from scripts.cameragroup import *
from scripts.tree import *
from scripts.tilemap import *
from scripts.enemy import *
from scripts.wavespawner import *

Clock = pygame.time.Clock()

class App:

    deltaTime = 0

    difficultyscalingspeed = 0.002
    difficultyscaling = 1
    tree_list = pygame.sprite.Group()

    def __init__(self):
        self._running = True
        self.screen = None
        self.size = self.weight, self.height = 1366, 768

    def on_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self.object_list = CameraGroup()

        #Create Tilemap
        self.tilemap = tilemap()
        self.enemies =  pygame.sprite.Group()

        #Start:
        self.player = Player(self.object_list, self.tree_list,self.enemies,'player.png',(0.1,0.1),False,0,150,10,2,100,0.5,self.tilemap)
        self.object_list.add(self.player)


        self.wavedelay = 15

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        for obj in self.object_list:
            obj.on_event(event)

    def on_loop(self):
        self.deltaTime = (Clock.tick(30)/1000)
        for obj in self.object_list:
            obj.on_loop(self.deltaTime)

        #waves
        self.difficultyscaling += self.difficultyscalingspeed*self.deltaTime
        self.wavedelay -= self.deltaTime * self.difficultyscaling
        if self.wavedelay <= 0:
            #start new wave
            newwave = wave(self.object_list,self.enemies,[
                enemy(self.object_list,self.tree_list,'player.png',(0.1,0.1),(0,0),20,self.player,3,300,1,5)
                ],
                (2,5),500)

            self.wavedelay = 15

        pass
    def on_render(self):
        self.screen.fill((0,0,0))
        self.object_list.draw_objects(self.player,self.deltaTime,self.tilemap) # draw player

        #UI
        self.addtexttoui('Apples: '+str(self.player.normalApples), (0,25), (255,50,50))
        self.addtexttoui('Seeds: '+str(self.player.seeds[0]), (0,50), (255,50,50))
        self.addtexttoui('HP: '+str(self.player.health), (0,self.height-100), (255,50,50))
        self.addtexttoui('Score: '+str(self.player.score), (self.weight/2-75,25), (255,50,50))
        #controls ui
        self.addtexttoui('Controls:', (self.weight-225,25), (255,75,75),25)
        self.addtexttoui('[WASD] to walk', (self.weight-225,50), (255,75,75),25)
        self.addtexttoui('[F] to plant', (self.weight-225,75), (255,75,75),25)
        self.addtexttoui('[M1] to shoot apple', (self.weight-225,100), (255,75,75),25)




        pygame.display.flip()

        pass
    def on_cleanup(self):
        pygame.quit()
    def addtexttoui(self, text, pos, color,fontsize = 32):
        font = pygame.font.Font('fonts/LilitaOne-Regular.ttf', fontsize)

        uitext = font.render(text,True, color)
        textRect = uitext.get_rect()
        textRect.midleft = pos
        self.screen.blit(uitext,textRect)

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
                #self.player.on_event(event)
            self.on_loop()
            self.on_render()
            #self.player.on_loop()
            #self.player.on_render()

        self.on_cleanup()

if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
