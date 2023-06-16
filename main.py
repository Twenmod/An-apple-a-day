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

        self.player = Player(self.object_list,self.enemies,'player.png',(0.1,0.1),False,0,100,100,1,100,1,self.tilemap)

        self.object_list.add(self.player)


        self.wavedelay = 20

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
        self.wavedelay -= self.deltaTime
        if self.wavedelay <= 0:
            #start new wave
            newwave = wave(self.object_list,self.enemies,[enemy(self.object_list,'player.png',(0.1,0.1),(0,0),20,self.player,2,100,1,5)])

            self.wavedelay = 20

        pass
    def on_render(self):
        self.screen.fill((0,0,0))
        self.object_list.draw_objects(self.player,self.deltaTime,self.tilemap) # draw player

        #UI
        font = pygame.font.Font('fonts/LilitaOne-Regular.ttf', 32)
        text = font.render('Apples: '+str(self.player.normalApples), True, (0,0,255))
        textRect = text.get_rect()
        self.screen.blit(text, textRect)
        text = font.render('Seeds: '+str(self.player.seeds[0]), True, (0,0,255))
        textRect = text.get_rect()
        textRect.centery = 50
        self.screen.blit(text, textRect)

        pygame.display.flip()

        pass
    def on_cleanup(self):
        pygame.quit()
 
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
