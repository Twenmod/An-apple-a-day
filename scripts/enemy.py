import os
import pygame
from pygame.locals import *
from scripts.gameobject import *
from scripts.projectile import *
from scripts.droppeditem import *

class enemy(gameObject):

    attackspeed = 1
    _attackcool = 0
    attackVelocity = 1
    attackDamage = 1
    walkspeed = 1
    target = None 
    slidedelay = 0
    currentslide = 0

    def __init__(self, object_list=None, tree_list = None, sprites=["Enemy0.png","Enemy1.png"], animationspeed=1, scale=(0.5,0.5), startposition=(0,0), walkspeed=1, player=None, attackspeed = 1, attackVelocity = 1, attackDamage = 1, maxhealth = 10, inaccuracy = 50):
        super().__init__(sprites[0], scale, True, 0, startposition)
        self.walkspeed = walkspeed
        self.target = player
        self.attackspeed = attackspeed
        self.attackVelocity = attackVelocity
        self.attackDamage = attackDamage
        self.object_list = object_list
        self.health = maxhealth
        self.tree_list = tree_list
        self.sprites = sprites
        self.scale = scale
        self.animationspeed = animationspeed
        self.inaccuracy = inaccuracy

    def on_loop(self, deltaTime):
        super().on_loop(deltaTime)

        #move to player
        playerdir = self.target.position - self.position
        if (playerdir.magnitude() > 0):
            playerdir = playerdir.normalize()
        self.position += playerdir * deltaTime * self.walkspeed

        #attack
        self._attackcool -= deltaTime
        if (self._attackcool <= 0):
            self._attackcool = self.attackspeed
            self.attack()

        self.slidedelay -= deltaTime
        if self.currentslide >= (len(self.sprites)):
            self.currentslide = 0
        elif (self.slidedelay <= 0):
            self.images = []
            img = pygame.image.load(os.path.join('images/', self.sprites[self.currentslide])).convert_alpha()
            img.set_colorkey(255)
            imgwidth = img.get_width()
            imgheight = img.get_height()
            imgsize = (imgwidth* self.scale[0], imgheight* self.scale[1]) 
            img = pygame.transform.scale(img, imgsize)
            self.images.append(img)
            self.image = self.images[0]
            self.currentslide += 1
            self.slidedelay = self.animationspeed

    def attack(self):

        playerdir = self.target.position - self.position
        if (playerdir.magnitude() > 0):
            playerdir = playerdir.normalize()

        proj = projectile(self.target,self.object_list, self.tree_list, 'Syringe.png', (1.6,1.6), 0, (self.rect.centerx,self.rect.centery), playerdir*self.attackVelocity, False, 5, 1)
        self.object_list.add(proj)
        pass
    def takedamage(self, damage):
        self.health -= damage
        if (self.health <= 0):
            # Spawn particle
            part = particle((2,2),True,0,(self.rect.topleft[0],self.rect.topleft[1]-25),["Enemy/Enemydeath0.png","Enemy/Enemydeath1.png","Enemy/Enemydeath2.png","Enemy/Enemydeath3.png"],0.2)
            self.object_list.add(part)
            #Drop seeds
            amountofitems = random.randrange(0,10)
            while(amountofitems > 0):
                drops = [None,None,None,None,None,None,droppeditem(self.target,'heart.png',(1,1),False,5,(self.rect.centerx,self.rect.centery),(random.randrange(-400,400),random.randrange(-400,400)),"heartPickup"),droppeditem(self.target,'seeds.png',(2.5,2.5),False,5,(self.rect.centerx,self.rect.centery),(random.randrange(-400,400),random.randrange(-400,400)),"normalSeeds"), droppeditem(self.target,'seeds.png',(2.5,2.5),False,5,(self.rect.centerx,self.rect.centery),(random.randrange(-200,200),random.randrange(-200,200)),"normalSeeds")]
                amountofitems-=1 
                drop = drops[random.randrange(0,len(drops),1)]
                if (drop != None):
                    self.object_list.add(drop)
            self.target.score += 15
            self.kill()
            #DIE