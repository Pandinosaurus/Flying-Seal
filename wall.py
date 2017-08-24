#Project : Flying-Seal
#File    : wall.py
#Author  : Remi Ratajczak
#Contact : Remi.Ratajczak@gmail.com

import os, pygame, sys, random
from colours import *

class Wall(pygame.sprite.Sprite):
        #Params
        GAP = 170               #hole to let the user pass
        GAPRATIO = 1./2.        #Used to randomly size upper and lower sides of the walls

        def __init__(self, screenHeight, screenwidth, width):
                #A wall is a sprite made of top, gap and bottom parts
                pygame.sprite.Sprite.__init__(self)

                #Random wall Gap position
                topHeight = random.randint(round((1./10.)*Wall.GAPRATIO*screenHeight), 
                                           round((1.0 - Wall.GAPRATIO)*screenHeight))
                bottomHeight = max(screenHeight - topHeight - Wall.GAP, 1)

                #Top wall
                self.top = pygame.Surface((width, topHeight))
                self.top.fill(brown)
                self.top_rect = self.top.get_rect()
                self.top_rect.y = 0
                
                #Bottom wall
                self.bottom = pygame.Surface((width, bottomHeight))
                self.bottom.fill(brown)
                self.bottom_rect = self.bottom.get_rect()
                self.bottom_rect.y = topHeight + Wall.GAP

                #Corresponding images
                self.image = pygame.Surface((width, screenHeight), pygame.SRCALPHA, 32)
                self.image.blit(self.top, (0,self.top_rect.y))
                self.image.blit(self.bottom, (0, self.bottom_rect.y))

                #Wall start to be at the most right position on the screen
                self.rect = self.image.get_rect()
                self.rect.x = screenwidth 

                #status flag ; false = alive = visible = to pass, true = dead = passed
                self.dokill = False;

        def update(self, speed):
                #The wall disappears from the screen at a given
                self.rect.x -= speed
                self.top_rect.x = self.rect.x #update
                self.bottom_rect.x = self.rect.x #update
                if self.rect.x < 0: #once the wall is unvisible, it means the player passed it -> set status flag
                        self.dokill = True
