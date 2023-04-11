import os
import pygame
from pygame.locals import *
from scripts.gameobject import *
from scripts.player import *
from scripts.camera import *
from scripts.cameragroup import *

Clock = pygame.time.Clock()

class App:
    def __init__(self):
        self._running = True
        self.screen = None
        self.size = self.weight, self.height = 1366, 768

    def on_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self.object_list = CameraGroup()

        #Start:
        self.player = Player('player.png',(0.1,0.1),False,0,0,1)
        self.mainCam = camera(self.player, 1,0.1,[self.weight,self.height])

        self.object_list.add(self.player)
 
        Object = gameObject('Box.png',(0.2,0.1),False,0,1,[50,50])
        Object.rect.x = 5
        Object.rect.y = 5
        self.object_list.add(Object)
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        for obj in self.object_list:
            obj.on_event(event)

    def on_loop(self):
        for obj in self.object_list:
            obj.on_loop()
        self.mainCam.on_loop()

        Clock.tick(60)

        pass
    def on_render(self):
        self.screen.fill((0,0,0))
        self.object_list.draw_objects(self.player) # draw player
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
