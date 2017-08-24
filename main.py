#Project : Flying-Seal
#File	 : main.py
#Author  : Remi Ratajczak
#Contact : Remi.Ratajczak@gmail.com
#
#ToDo :
# *put Game() class in another file
# *put rename welcomScreen in enterNameScreen and put it in another class/file
# *add a titleScreen
# *add sounds
# *create separated structures for each levels (background, to change walls skins + sounds)
# *simplify the names and comments in wall.py
# *fix issue on MacOs : game far more (too) slow compared with linux and windows

import os, pygame, sys, random
from pygame import *	#the big lib
from colours import *   #contain the colors
from highscore import * #the highscore view + manager
from wall import * 	#the obstacles
from player import *	#the player

class Game:
	def init(self):
		pygame.mixer.init(22050,-16,2,16)
		pygame.init()
		self.setIcon()
		self.reset()

	def setIcon(self):
		icon = pygame.image.load("./ressources/Players/SealDraw.png")
		pygame.display.set_icon(icon)

	def reset(self):
		self.initStatus()
		self.initScreen()
		self.initBackground()
		self.initUser()
		self.initScore()
		self.initText()

	def resetButUser(self):
		self.initStatus()
		self.initScreen()
		self.initBackground()
		self.initScore()
		self.initText()

	def initStatus(self):
		self.FPS = 60
		self.STARTED = False
		self.HIT = False
		self.SPEED = 6

	def initScreen(self):
		self.SCREENWIDTH = 300
		self.SCREENHEIGHT = 400
		self.SCREEN = pygame.display.set_mode((self.SCREENWIDTH, self.SCREENHEIGHT), 
						       HWSURFACE | DOUBLEBUF | RESIZABLE)
		self.MAINFONT = pygame.font.SysFont('Arial',16, True)
	
	def initBackground(self):
		self.BACKGROUNDSIZEFACTOR = 3
		self.BACKGROUNDWIDTH = self.SCREENWIDTH*self.BACKGROUNDSIZEFACTOR
		self.BACKGROUNDHEIGHT = self.SCREENHEIGHT
		self.BACKGROUNDSCROLLINGSPEED = 0
		self.BACKGROUNDDIR = "./ressources/Backgrounds/"
		self.BACKGROUNDNAME = "Background"
		self.BACKGROUNDEXT = ".bmp"
		self.NBOFBACKGROUNDS = self.countFilesInDir(self.BACKGROUNDDIR)
		self.setBackgroundPic()

	def initUser(self):
		self.USERNAME = "AAA"
		self.updateUsernameText( cyan )
		self.setPlayers()  

	def initScore(self):
		self.SCORE = 0
		self.HIGHSCOREPATH = "./ressources/Highscores/highscores.txt"
		self.updateScoreText( black )

	def initText(self):
		self.setEnterText('Enter your name', red)
		self.setStartText('Press "space" to start', black)
		self.setUsernameText( self.USERNAME, cyan )
		self.setScoreText( self.SCORE, black )
	
	def setBackgroundPic(self):
		self.BACKGROUNDPIC = pygame.image.load(self.BACKGROUNDDIR + 
						       self.BACKGROUNDNAME + 
						       str(random.randint(0,self.NBOFBACKGROUNDS-1))+
						       self.BACKGROUNDEXT)
		self.BACKGROUNDPIC = pygame.transform.scale(self.BACKGROUNDPIC, (self.BACKGROUNDWIDTH, 								
										 self.BACKGROUNDHEIGHT))
		self.BACKGROUNDPIC = self.BACKGROUNDPIC.convert()#video system has to be initialed

	def setPlayers(self):
		#Set a sprite for the player(s)
		self.PLAYERSIZE = (80,40)
		self.PLAYERSKINPATH = "./ressources/Players/SealDraw.png"
		self.PLAYERJUMPVELOCITY = 14
		self.PLAYERGRAVITY = 0.81
		self.PLAYER = Player(self.PLAYERSIZE, 
				     self.PLAYERSKINPATH, 
				     self.PLAYERJUMPVELOCITY, 
		  		     self.PLAYERGRAVITY)
		self.PLAYERS = pygame.sprite.RenderUpdates()
		self.PLAYERS.add(self.PLAYER)

	def setObstacles(self):
		#Set sprites for the obstacles - actually added when timer reached limit
		self.WALLS = pygame.sprite.RenderUpdates()
		self.WALLSTIMER = 0
		self.WALLSINTERVAL = 80
		self.WALLSWIDTH = 35
		
	def setEnterText( self, text, color ):
		self.ENTERTEXT = self.MAINFONT.render(str(text), False, color)

	def setStartText( self, text, color ):
		self.STARTTEXT = self.MAINFONT.render(str(text), False, color)

	def setUsernameText( self, text, color ):
		if text != self.USERNAME:
			self.USERNAME = str(text)
		self.USERNAMETEXT = self.MAINFONT.render(str(text), False, color)

	def setScoreText( self, text, color ):
		if int(text) != self.SCORE:
			self.SCORE = int(text)	
		self.SCORETEXT = self.MAINFONT.render(str(text), False, color)  

	def updateUsernameText( self, color ):
		self.USERNAMETEXT = self.MAINFONT.render(str(self.USERNAME), False, color)
	
	def updateScoreText( self, color ):
		self.SCORETEXT = self.MAINFONT.render(str(self.SCORE), False, color)  

	def countFilesInDir(self,dir):
		return len([name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir, name))])
	
	def updateDisplay(self):
		pygame.display.flip() 
		pygame.display.update()

	#User nickname input - NB : replace self.USERNAME with a local variable for genericity purpose
	def welcomeScreen(self):
		self.reset()
		done   = True
		while done:
			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					pygame.quit()
					quit()
				if event.type == pygame.KEYDOWN:
					key = event.key
					if   key == pygame.K_RETURN:
						done = False
					elif key == pygame.K_BACKSPACE:
						if   len(self.USERNAME) > 0:
							self.USERNAME = self.USERNAME[:-1]
					elif key != pygame.K_BACKSPACE and key != pygame.K_SPACE:
						if   len(self.USERNAME) > 0:
							self.USERNAME += str(chr(key)) 
						elif key < 256: #max char value
							self.USERNAME  = str(chr(key))
			#Update texts
			self.updateUsernameText( cyan )

			#fill screen view
			self.SCREEN.fill( black )
			self.SCREEN.blit(self.ENTERTEXT,(self.SCREENWIDTH/2  - self.ENTERTEXT.get_width()/2,
							 self.SCREENHEIGHT/2 - self.ENTERTEXT.get_height()))
			self.SCREEN.blit(self.USERNAMETEXT,(self.SCREENWIDTH/2  - self.USERNAMETEXT.get_width()/2,
							    self.SCREENHEIGHT/2 + self.USERNAMETEXT.get_height())) 
			#display
			self.updateDisplay()

		self.playScreen()

	def playScreen(self):
		self.setBackgroundPic()
		self.setPlayers()
		self.setObstacles()
		self.playLoop()

	def playLoop(self):
		self.resetButUser()
		while True:
			#Set clock for fps purpose
		  	clock = pygame.time.Clock()

			#Check if we should wait a user action before to play
			if self.STARTED == False:
				self.waitForStart()

			#Check if player hurt an obstacle
			if self.HIT == True: 
				self.highscoreScreen()
		
			#jump if user decided to jump
			self.doJump()

			#add wall obstacles 
			self.doWall()

			#Set the next background frame (scrolling)
			self.doScroll()
	
			#Update the sprites (player that jumped and the obstacles)
			self.doSpritesUpdate()	
		
			#Check if user failed
			self.doCheckFailed()
		
			#Set the score
			self.doScore()  	
	
			#Render elements
			self.doRender()

			#Update the view
			self.updateDisplay()

			#Wait a few milliseconds
			clock.tick(self.FPS)

	def waitForStart(self):
		if not self.STARTED :
			#Show play screen for the first time	
			self.SCREEN.blit(self.BACKGROUNDPIC, (0, 0))
			self.SCREEN.blit(self.STARTTEXT,(self.SCREEN.get_width()  / 2   - self.STARTTEXT.get_rect()[2] / 2,
					      	 	 self.SCREEN.get_height() / 1.5 - self.STARTTEXT.get_rect()[3] / 2))
			while not self.STARTED:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()
					if event.type == pygame.KEYDOWN:
						if event.key == K_SPACE:
							self.STARTED = True
							self.jump()
				self.updateDisplay()
	
	def jump(self):
		self.PLAYER.jump()
		self.PLAYER.rect.clamp_ip(self.SCREEN.get_rect())
	
	def highscoreScreen(self):
			#Display highscore SCREEN - no need to keep it in class
			#only called when user fail
			#plus it reload when score is added 
			highscore = Highscore( self.HIGHSCOREPATH )	
			highscore.addScore(self.USERNAME, self.SCORE )
			highscore.displayScore(self.SCREEN.get_width(),
					       self.SCREEN.get_height())
			#Restart
			self.playScreen()
			

	def doJump(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self.jump()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				self.jump()		

	def doWall(self):
		#Add obstacles if timers reached obstacles limits
		self.WALLSTIMER +=1
		if self.WALLSTIMER >= self.WALLSINTERVAL:
			self.WALLSTIMER = 0
			self.WALLS.add(Wall(self.SCREEN.get_height(), 
					    self.SCREEN.get_width(),
					    self.WALLSWIDTH))

	def doScroll(self):
		self.BACKGROUNDSCROLLINGSPEED -= self.SPEED/3
		if self.BACKGROUNDSCROLLINGSPEED <= self.BACKGROUNDWIDTH * -1: 
			self.BACKGROUNDSCROLLINGSPEED = 0

	def doSpritesUpdate(self):
		self.PLAYERS.update()
		self.WALLS.update( self.SPEED )	

	def doCheckFailed(self):
		#Check if user falled
		if self.PLAYER.rect.y > self.SCREENHEIGHT:
			self.HIT = True
		#Check for collides and remove passed walls
		for w in self.WALLS:
			if w.dokill == True:
				self.WALLS.remove(w)
				self.SCORE += 1
			if self.PLAYER.rect.colliderect(w.top_rect) or self.PLAYER.rect.colliderect(w.bottom_rect): 
				self.HIT = True

	def doScore(self):
		self.updateScoreText( black )  

	def doRender(self):
		#Draw sprites display
		self.SCREEN.blit(self.BACKGROUNDPIC, (self.BACKGROUNDSCROLLINGSPEED, 0))
		self.SCREEN.blit(self.BACKGROUNDPIC, (self.BACKGROUNDSCROLLINGSPEED + self.BACKGROUNDWIDTH, 0))
		self.SCREEN.blit(self.SCORETEXT, (5, 5))
		self.PLAYERS.draw(self.SCREEN)
		self.WALLS.draw(self.SCREEN)

	def run(self):
		self.welcomeScreen()		
		
if __name__ == '__main__':
	g = Game()
	g.init()
	g.run()
