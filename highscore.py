#Project : Flying-Seal
#File    : highscore.py
#Author  : Remi Ratajczak
#Contact : Remi.Ratajczak@gmail.com

import sys, pygame
from colours import *

#Load, update and display highscores
#Format: name score \n
class Highscore:
        def __init__(self, path):
                #Make sure pygame has been activated
                pygame.init()
                
                #Highscore path
                self.path = path

                #Set variables
                self.textSize = 16
                self.usernameLength = 13
                self.maxNbOfHighscores = 5
                self.bestHighscore = -1
                self.worstHighscore = -1
                self.latestScore = 0
                self.currentUsername = "AAA"

                #Init model             
                self.reloadScoreData()
        
        def reloadScoreData(self):
                #renew score table
                self.scores = []

                #load file in memory and read it
                file = open(self.path,"r").readlines()
                
                #work with temporary score table
                scores = []
                row = 0
                for line in file:
                        scores.append(line)
        
                #sort scores using second word as a key thanks to split()
                #NB : spaces count for nothing
                scores.sort(key=lambda score: int(score.split()[1]))
                scores.reverse()

                #Keep the 10 best scores in the class
                for idx in range(0, min(len(scores),self.maxNbOfHighscores)):
                        self.scores.append( scores[idx] )

                #Save best and worst highscores
                if len(scores) >= 1:
                        self.worstHighscore = int( self.scores[len(self.scores)-1].split()[1])
                        self.bestHighscore = int(self.scores[0].split()[1])
        
        def addScore(self,username,score):
                #Update the current username value
                self.currentUsername = username

                #Add a highscore only if it is higher than a previous one
                if score >= self.worstHighscore:

                        #Open the highscore file
                        file = open(self.path,"a")

                        #Write username and score in highscore file
                        file.write(str(self.currentUsername)+" "+str(score)+" "+"\n")

                        #Update the model
                        self.reloadScoreData()
                
                #Update latest score
                self.latestScore = score
        
        def displayScore(self, width, height):
                #Init a screen
                self.screen = pygame.display.set_mode((width, height))
                self.clearBackground()

                #Make sure you show the latest values / model
                self.reloadScoreData()

                #Adapt font size to screen based on Highscores title text
                font = pygame.font.SysFont('Arial',self.textSize, True)
                sampleText = font.render("SAMPLE", False, yellow)
                while max(width/2 - sampleText.get_rect()[2]/2 - self.usernameLength*self.textSize/2,5) == 5:
                        self.textSize = self.textSize - 1
                        font = pygame.font.SysFont('Arial',self.textSize, True)
                        sampleText = font.render("SAMPLE", False, yellow)
                textHeight = sampleText.get_rect()[3];          

                #Print highscores title
                indx= 0
                highscoreText = font.render("Highscores", False, yellow)
                self.screen.blit(highscoreText, (width/2   - highscoreText.get_rect()[2]/2, 
                                                 height/10 + 2*self.textSize*indx - textHeight/2))
                
                #Print highscores and color the current added one if value exist
                indx = 1
                colored = False
                for score in self.scores:       
                        scoreColor = cyan
                        if int(score.split()[1]) == self.latestScore:
                                if str(score.split()[0]) == str(self.currentUsername):
                                        if colored == False:
                                                scoreColor = red
                                                colored= True                           
                        usernameText = font.render(str(score.split()[0]), False, scoreColor)
                        scoreText    = font.render(str(score.split()[1]), False, scoreColor)
                        self.screen.blit(usernameText, (width/2   - self.textSize*self.usernameLength/2, 
                                                        height/10 + 2*self.textSize*indx - textHeight/2))
                        self.screen.blit(scoreText,    (width/2   + self.textSize*self.usernameLength/4, 
                                                        height/10 + 2*self.textSize*indx - textHeight/2))                                       
                        indx += 1
                #indx should be equal to 6              

                #Print score
                indx += 2
                if self.latestScore >= self.worstHighscore:
                        newHighscoreText = font.render("NEW HIGHSCORE ACHIEVED", False, yellow)
                        self.screen.blit(newHighscoreText, (width/2   - newHighscoreText.get_rect()[2]/2, 
                                                            height/10 + 2*self.textSize*indx - textHeight/2))
                else:           
                        yourScoreText = font.render("Your score is : "+str(max(self.latestScore,0)), False, yellow)
                        self.screen.blit(yourScoreText, (width/2   - yourScoreText.get_rect()[2]/2, 
                                                        height/10 + 2*self.textSize*indx - textHeight/2))
                #indx should equal to 8

                #Print retry message
                indx += 2
                retryText = font.render('Press any key to try again', False, cyan)
                self.screen.blit(retryText, (width/2    - retryText.get_rect()[2]/2, 
                                             height/10 + 2*self.textSize*indx - textHeight/2))

                #indx should be equal to 10

                #Load the view
                pygame.display.flip()
                
                exit = False
                while not exit:
                        for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                        pygame.quit()
                                        sys.exit()
                                elif event.type == pygame.MOUSEBUTTONDOWN:
                                        exit = True
                                elif event.type == pygame.KEYDOWN:
                                        exit = True

        def clearBackground(self):
                bg = pygame.Surface(self.screen.get_size())
                bg = bg.convert()
                bg.fill((0,0,0))
                self.screen.blit(bg,(0,0))

        def printText(self,text,point):
                font = pygame.font.SysFont("Arial", self.textSize, True)
                label = font.render(str(text)+'  ', True, (255,255, 255), (0, 0, 0))
                textRect = label.get_rect()
                textRect.x = point[0] 
                textRect.y = point[1]
                self.screen.blit(label, textRect)
