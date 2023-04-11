import os
import pygame
from pygame.locals import *
from gameobject import *
from player import *
from camera import *

Clock = pygame.time.Clock()

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 1366, 768

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.screen = self._display_surf.copy()
        self._running = True
        self.object_list = pygame.sprite.Group()

        #Start:
        self.player = Player('player.png',(0.1,0.1),False,0,0,1)
        self.mainCam = camera(self.player, 1,0.1,[self.weight,self.height])

        self.object_list.add(self.player)
 
        #Gameobject test
        #Object = gameObject('player.png',(0.5,0.5),False,0,0.1)
        #Object.rect.x = 0
        #Object.rect.y = 0
        #self.object_list.add(Object)
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        for obj in self.object_list:
            obj.on_event(event)

    def on_loop(self):
        for obj in self.object_list:
            obj.on_loop()
        self.mainCam.on_loop()

        pass
    def on_render(self):
        self.screen.fill((0,0,0))
        self.screen.blit(pygame.image.load("images/grid.png"),(-self.mainCam.position[0],-self.mainCam.position[1]))
        self.object_list.draw(self.screen) # draw player
        self._display_surf.blit(pygame.transform.scale(self.screen, self.screen.get_rect().size*self.mainCam.zoom), (-self.mainCam.position[0]+(self.weight/2), -self.mainCam.position[1]+(self.height/2)))
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
