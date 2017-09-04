#Project : Flying-Seal
#File    : main.py
#Author  : Remi Ratajczak
#Contact : Remi.Ratajczak@gmail.com
#
#This is just an interface for the user
#Go to game.py for the logic

import os, sys, random
from game import *      
                
if __name__ == '__main__':
        g = Game()
        g.run()
