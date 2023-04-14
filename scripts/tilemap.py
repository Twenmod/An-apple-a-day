import os
import pygame
from pygame.locals import *

class tileType():
    def __init__(self, type = "G", spritepath = "Box.png") -> None:
        self.type = type
        self.spritepath = "world/"+spritepath
        pass


class tile(pygame.sprite.Sprite):
    def __init__(self, sprite = 'Box.png', scale = (1, 1), startposition = (0,0)):
        print("I AM NOW EXIST AT: "+str(startposition))
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

    tiletypes = [tileType("G","Grass.png"),tileType("D","Dirt.png")]

    map = [
        "GGGGGGGGGG",
        "GGGGGGGGGG",
        "GGGGGGGGGG",
        "GGDDDGGGGG",
        "GDDGDGGGGG",
        "GGDDDGGGGG",
        "GGDGDGGGGG",
        "GGGGGGGGGG",
        "GGGGGGGGGG",
        "GGGGGGGGGG",
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
                
                spawned = tile(ttype.spritepath,(0.5,0.5),(xpos, ypos))
                tileline.append(spawned)
                self.tileobjects.append(spawned)
                xpos += self.tilesize
            ypos += self.tilesize

            self.tiles.append(tileline)
        pass
    pass