import os
import pygame
from pygame.locals import *
import random

class tileType():
    def __init__(self, type = "G", spritepaths = ["Box.png"], plantable=False) -> None:
        self.type = type
        self.spritepaths = spritepaths
        self.plantable = plantable
        pass


class tile(pygame.sprite.Sprite):
    def __init__(self, sprites = ['Box.png'], scale = (1, 1), startposition = (0,0),plantable=False):
        print("I AM NOW EXIST AT: "+str(startposition))
        sprite = sprites[random.randrange(0,len(sprites),1)]
        self.plantable = plantable
        pygame.sprite.Sprite.__init__(self)
        self.images = []

        img = pygame.image.load(os.path.join('images', sprite)).convert_alpha()
        img.set_colorkey(255)
        imgwidth = img.get_width()
        imgheight = img.get_height()
        imgsize = (imgwidth* scale[0], imgheight* scale[1]) 
        img = pygame.transform.scale(img, imgsize)
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = startposition[0]
        self.rect.y = startposition[1]
        pass

    pass

class tilemap():

    tiletypes = [tileType("G",["world/grass0.png","world/grass1.png","world/grass2.png","world/grass3.png","world/grass4.png","world/grass5.png","world/grass6.png"], False),tileType("D",["world/dirt0.png","world/dirt1.png","world/dirt1.png","world/dirt2.png","world/dirt2.png","world/dirt3.png","world/dirt3.png","world/dirt4.png","world/dirt5.png","world/dirt6.png","world/dirt7.png","world/dirt7.png","world/dirt8.png","world/dirt9.png","world/dirt10.png","world/dirt11.png"], True)]

    plantabletiles = []

    map = [
        "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
        "GGGGDDDDGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
        "GGGGGDDDDGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGDDDDDD",
        "GGGGGGGDDGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGDDGDD",
        "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGDDDGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGDDGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGDDDGGGGGGGGGGGGGDDGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGDDDDGGGGGGGGGGGGGGGGDDDDGGGGGGG",
        "GGGGGGDDGGGGGGDDDDGGGGGGGGGGGGGGGDDDDDDGGGGGGG",
        "GGGGGGDDDDGGGGGGGGGGDDGGGGGGGGGGGGGGGGGGGDDGGG",
        "GGGGGGGGGGGGGGGGGGGDDDDGGGGGGGDDGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGDGGGGGDDDDGGGGGGGDDDGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGDDGGGGGGGGGGGGGGGDDGGGGGGGGGGGGGG",
        "GGGGGGGGGDDGGGGGGGGGGDGGGGGGGGGGGGGGGDDDDGGGGG",
        "GGGGGGGGDDDGGGGGGGGGGGGGDDDGGGGGGGGGGGDDGGGGGG",
        "GGGGGGGGDDGGGGGGGGGGGGGGDDDGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGDDDDDGGGGGGDDGGGGGGGGDDDGGGGGGGG",
        "GGGGGGGGGGGGGDDDDDDGGDDDGGGGGGGGGGDDDDGGGGGGGG",
        "GGGGGGGGGGGGGGDDDDGGDDGDGGGGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGGGDDDGGGGGGGDDDGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGGGDGDGGGGGGDDDDGGGGGGGGGGGG",
        "GGGGGGGGGGGGGDDDGGGGGGGGGGGGGGDDDDGGGGGGGGGGGG",
        "GGGGGGGGGGGGDDDDGGGGGGGGGGGGGGGDDDGGGGGGGGGGGG",
        "GGGGGGGGGGGGGDDDGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGGDDDDDGGGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGDDDDDDDDGGGGGGGGGDDDGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGDDDDDGGGGGG",
        "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGDDGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",




    ]

    tiles = [[]]
    tileobjects = []

    tilesize = 50

    def __init__(self) -> None:
        #spawn all tiles
        ypos = 0
        for y in self.map:
            tileline = []
            xpos = 0
            for x in y:
                ttype = None
                for types in self.tiletypes:
                    if (types.type == x):
                        ttype = types
                
                spawned = tile(ttype.spritepaths,(2,2),(xpos, ypos),ttype.plantable)
                if (spawned.plantable):
                    self.plantabletiles.append(spawned)
                tileline.append(spawned)
                self.tileobjects.append(spawned)
                xpos += self.tilesize
            ypos += self.tilesize

            self.tiles.append(tileline)
        pass
    pass