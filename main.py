import os
import pygame
import random as rng
from pygame.locals import *
from scripts.gameobject import *
from scripts.player import *
from scripts.cameragroup import *
from scripts.tree import *
from scripts.tilemap import *
from scripts.enemy import *
from scripts.wavespawner import *

Clock = pygame.time.Clock()

global score
score = 0
global highscore
highscore = 0

class App:
    gamerunning = False
    endscreen = False
    def __init__(self):
        self._running = True
        self.screen = None
        self.size = self.weight, self.height = 1366, 768
    def on_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
    def on_loop(self):
        pass
    def on_event(self, event):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE] or event.type == pygame.QUIT:
            self._running = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            self.startgame()
        pass
    def on_render(self):
        if not self._running: return
        self.screen.fill((75,255,75))
        bg = pygame.image.load("images/Mainmenu.png").convert_alpha()
        self.screen.blit(bg,bg.get_rect())

        if (self.endscreen):
            self.addtexttoui("You died",(self.weight/2-125,self.height/2-100),(255,0,0),62)
            global score
            self.addtexttoui("Score: "+str(score),(self.weight/2-80,self.height/2-50),(255,0,0),42)
            global highscore
            self.addtexttoui("Highscore: "+str(highscore),(self.weight/2-80,self.height/2-15),(255,0,0),32)

        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()
    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while( self._running and not self.gamerunning):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()

        self.on_cleanup()
    def addtexttoui(self, text, pos, color,fontsize = 32):
        font = pygame.font.Font('fonts/LilitaOne-Regular.ttf', fontsize)

        uitext = font.render(text,True, color)
        textRect = uitext.get_rect()
        textRect.midleft = pos
        self.screen.blit(uitext,textRect)

    def startgame(self):
        self.gamerunning = True
        theApp = Mainlevel(self.screen)
        theApp.on_execute()
        self.endscreen = True
        print("Ended game?")
        self.gamerunning = False
        self.__init__()
        self.on_init()

class Mainlevel:

    deltaTime = 0

    difficultyscalingspeed = 0.002
    difficultyscaling = 1

    startdowntime = 15

    tree_list = pygame.sprite.Group()

    def __init__(self, screen):
        self._running = True
        self.screen = screen
        self.size = self.weight, self.height = 1366, 768

    def on_init(self):
        self.screen.fill((0,0,255))
        self._running = True
        self.object_list = CameraGroup()

        #Create Tilemap
        self.tilemap = tilemap()
        self.enemies =  pygame.sprite.Group()

        #Start:
        self.player = Player(self.object_list, self.tree_list,self.enemies,'player.png',['playerstep0.png','playerstep1.png'],(0.1,0.1),False,0,150,10,2,100,0.5,self.tilemap)
        self.object_list.add(self.player)


        self.wavedelay = 0

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.endgame()
        for obj in self.object_list:
            obj.on_event(event)

    def on_loop(self):
        self.deltaTime = (Clock.tick(30)/1000)

        if self.player.health <= 0:
            self.endgame()

        for obj in self.object_list:
            obj.on_loop(self.deltaTime)

        self.startdowntime -= self.deltaTime
        if (self.startdowntime <= 0):
            #waves
            self.difficultyscaling += self.difficultyscalingspeed*self.deltaTime
            self.difficultyscaling = pygame.math.clamp(self.difficultyscaling,0,7.5)
            self.wavedelay -= self.deltaTime * self.difficultyscaling
            if self.wavedelay <= 0:
                #start new wave
                newwave = wave(self.object_list,self.enemies,[
                    enemy(self.object_list,self.tree_list,["Enemy0.png","Enemy1.png"],0.5,(2,2),(0,0),20,self.player,3,200,1,5)
                    ],
                    (2,5),1000)

                self.wavedelay = rng.randrange(0,30,1)

        pass
    def on_render(self):
        self.screen.fill((97,184,117))
        self.object_list.draw_objects(self.player,self.deltaTime,self.tilemap) # draw player

        #UI
        self.addtexttoui('Apples: '+str(self.player.normalApples), (0,25), (255,50,50))
        self.addtexttoui('Seeds: '+str(self.player.seeds[0]), (0,50), (255,50,50))
        self.addtexttoui('HP: '+str(self.player.health), (0,self.height-100), (255,50,50))
        self.addtexttoui('Score: '+str(self.player.score), (self.weight/2-75,25), (255,50,50))
        #controls ui
        self.addtexttoui('Controls:', (self.weight-250,25), (255,75,75),25)
        self.addtexttoui('[WASD] to walk', (self.weight-250,50), (255,75,75),25)
        self.addtexttoui('[M1] to shoot apple', (self.weight-250,75), (255,75,75),25)
        self.addtexttoui('[E] to harvest', (self.weight-250,100), (255,75,75),25)
        self.addtexttoui('[F] to plant', (self.weight-250,125), (255,75,75),25)
        self.addtexttoui('(1 seed)', (self.weight-250,145), (255,75,75),15)
        self.addtexttoui('[G] to plant MEGA tree', (self.weight-250,165), (255,75,75),25)
        self.addtexttoui('(10 seeds)', (self.weight-250,185), (255,75,75),15)



        pygame.display.flip()

        pass
    def on_cleanup(self):
        pass
    def addtexttoui(self, text, pos, color,fontsize = 32):
        font = pygame.font.Font('fonts/LilitaOne-Regular.ttf', fontsize)

        uitext = font.render(text,True, color)
        textRect = uitext.get_rect()
        textRect.midleft = pos
        self.screen.blit(uitext,textRect)
    def endgame(self):
        global score
        score = self.player.score
        global highscore
        if (score > highscore):
            highscore = score
        self._running = False
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
