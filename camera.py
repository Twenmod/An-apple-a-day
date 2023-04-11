import os
import pygame
from pygame.locals import *
from gameobject import *
from math import *

class camera():
    followObject = gameObject
    position = [0,0]
    smoothTime = 0.1
    zoom = 1
    resolution = [0,0]

    def __init__(self, objectToFollow = gameObject, zoom = 10, smooth = 0.1, resolution = [1366,768]):
        self.followObject = objectToFollow
        self.smoothTime = smooth
        self.zoom = zoom
        self.resolution = resolution
    def on_loop(self):
        self.position[0] = lerp(self.position[0],self.followObject.position[0],self.smoothTime)
        self.position[1] = lerp(self.position[1],self.followObject.position[1],self.smoothTime)
        print("Player: " + str(self.position[0])+str(self.position[1]))

        pass
    def on_event(self, event):
        pass


def lerp(a: float, b: float, t: float) -> float:
    return (1 - t) * a + t * b