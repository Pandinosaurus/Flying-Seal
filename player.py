#Project : Flying-Seal
#File    : player.py
#Author  : Remi Ratajczak
#Contact : Remi.Ratajczak@gmail.com

import os, pygame, sys, random
from colours import *

class Player(pygame.sprite.Sprite):
        def __init__(self, size, skinpath, jump_velocity, g, file = None):
                #A player is a sprite
                pygame.sprite.Sprite.__init__(self)

                #Set vertical velocities : jump, gravity and current velocity
                self.jump_velocity = jump_velocity
                self.g = g 
                self.velocity = 0

                #Skin           
                self.image = pygame.image.load(skinpath)
                self.image = pygame.transform.scale(self.image,size)
                self.rect = self.image.get_rect()

        def jump(self):
                #Going up is going in the negative (0,0 based on left,top)
                self.velocity = self.jump_velocity * -1

        def update(self):
                self.rect.y += round(self.velocity) #if > 0, go down, else go up
                self.velocity += self.g #make sure gravity is set back after a jump
