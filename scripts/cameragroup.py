import os
import pygame
from pygame.locals import *

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2


        self.ground_surf = pygame.image.load('images/world/Grid.png').convert()
        self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))


    def center_target_camera(self,target, lerpspeed, deltaTime):
        self.offset.x = lerp(self.offset.x, target.rect.centerx - self.half_w, lerpspeed*deltaTime)
        self.offset.y = lerp(self.offset.y, target.rect.centery - self.half_h, lerpspeed*deltaTime)

    cullRadius = 200

    def draw_objects(self, player, deltaTime, tilemap):
        self.center_target_camera(player, 2, deltaTime)
        #ground
        for sprite in tilemap.tileobjects:
            self.display_surface.blit(sprite.image,sprite.rect.topleft - self.offset)
        #objects
        for sprite in sorted(self.sprites(),key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            if not (offset_pos.x < -self.cullRadius or offset_pos.x > self.half_w*2+self.cullRadius or offset_pos.y < -self.cullRadius or offset_pos.y > self.half_h*2+self.cullRadius):
                self.display_surface.blit(sprite.image,offset_pos)


def lerp(a: float, b: float, t: float) -> float:
    return (1 - t) * a + t * b