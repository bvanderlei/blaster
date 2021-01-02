# -*- coding: utf-8 -*-
"""
Created on Tues Dec 15 17:12:35 2020
s
@author: Ben Vanderlei
"""

import pygame
import random

WHITE = 255,255,255


class Block(pygame.sprite.Sprite):
    
    def __init__(self,color,width,height):
        super().__init__()
        
        self.image = pygame.Surface([width,height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.vx = 0
        self.vy = 0

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

class Rock(pygame.sprite.Sprite):

    def __init__(self,sheet):
        super().__init__()

        self.images = []
        self.images.append(sheet.get_image(0,0,16,16))
        self.images.append(sheet.get_image(0,16,16,16))
        self.images.append(sheet.get_image(0,32,16,16))
        self.images.append(sheet.get_image(0,48,16,16))        

        self.frames = len(self.images)
        self.index = random.randint(0,self.frames-1)
        
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
#        self.vx = random.randint(-1,1)
        self.vx = 0
        self.vy = 1

        self.tick = 0
        
    def update(self,screen_width,screen_height):
        self.rect.x += self.vx
        self.rect.y += self.vy
        
        self.tick += 1
        if (self.tick == 5):
            self.tick = 0
            self.index = (self.index+1)%self.frames
            self.image = self.images[self.index]
        
        
class Ship(pygame.sprite.Sprite):
    
    def __init__(self,sheet):
        super().__init__()

        self.images = []
        self.images.append(sheet.get_image(0,0,32,32))
        self.images.append(sheet.get_image(0,32,32,32))
        self.images.append(sheet.get_image(0,64,32,32))

        self.index = 0
        self.frames = len(self.images)
        
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.vx = 0
        self.vy = 0

        self.tick = 0
        self.blast = False
        
    def update(self,screen_width,screen_height):
        if self.rect.x > 3 and self.vx < 0:
            self.rect.x += self.vx
        if self.rect.x < screen_width - 32 and self.vx > 0:
            self.rect.x += self.vx
        if self.rect.y < screen_height - 36 and self.vy > 0:
            self.rect.y += self.vy
        if self.rect.y > screen_height - 100 and self.vy < 0:
            self.rect.y += self.vy
        
        self.tick += 1
        if (self.tick == 3):
            self.tick = 0
            self.index = (self.index+1)%self.frames
            self.image = self.images[self.index]

class Bullet(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = pygame.Surface([3,10])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.vx = 0
        self.vy = 0

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        


class SpriteSheet(object):

    def __init__(self, file_name):
        ## Constructor.  Pass in filename of the sprite sheet."
        self.sprite_sheet = pygame.image.load(file_name)

    def get_image(self,x,y,width,height):
        """ Get a single image out of the sheet. """

        image = pygame.Surface([width,height])
        image.blit(self.sprite_sheet,(0,0),(x,y,width,height))
        image.set_colorkey((0,0,0))
        return image
