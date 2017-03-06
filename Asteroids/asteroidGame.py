'''
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
#####
Rylan Denis
Mr. Davis
Asteroids
2/27/2017
Adv. Comp. Prog.
Version 1.2
'''

import pygame, sys, random
from pygame.locals import *

pygame.init()

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

background = BLACK
entity_color = WHITE

background=pygame.image.load("space.jpg")
listAsteroid=[]
listLaser=[]
leveltime=50
creationTime=leveltime
all_sprites_list = pygame.sprite.Group()
lives=3
score=0

#Collision Detection
def isPointInsideRect(x,y,rect):
    if (x>rect.left) and (x<rect.right) and (y>rect.top) and (y<rect.bottom):
        return True
    else:
        return False

def doRectOverlap(rect1,rect2):
    for a,b in [(rect1,rect2),(rect2,rect1)]:
        if ((isPointInsideRect(a.left,a.top,b)) or
                (isPointInsideRect(a.left,a.bottom,b)) or
                (isPointInsideRect(a.right,a.top,b)) or
                (isPointInsideRect(a.right,a.bottom,b))):
            return True
    return False

#----------------------------------------------
#CLASSES
#----------------------------------------------
class Entity(pygame.sprite.Sprite):
    """Inherited by any object in the game."""

    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # This makes a rectangle around the entity, used for anything
        # from collision to moving around.
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class Ship(Entity):
    """
    Player controlled or AI controlled, main interaction with
    the game
    """

    def __init__(self, x, y, width, height):
        super(Ship, self).__init__(x, y, width, height)

        self.image = pygame.image.load('spaceship.png')
        ship = pygame.image.load('spaceship.png')
        self.image.blit(ship, (0, 0))



class Player(Ship):
    """The player controlled Ship"""

    def __init__(self, x, y, width, height):
        super(Player, self).__init__(x, y, width, height)

        # How many pixels the Player Ship should move on a given frame.
        self.y_change = 0
        # How many pixels the Ship should move each frame a key is pressed.
        self.y_dist = 5
        #Check if the player is still alive
        self.killed=False

    def MoveKeyDown(self, key):
        """Responds to a key-down event and moves accordingly"""
        if (key == pygame.K_SPACE) and self.killed==False:
            x = Laser(player.rect.x + 20, player.rect.y + 18, 20, 5)
            all_sprites_list.add(x)
            listLaser.append(x)
            laserSound.play()
        elif (key == pygame.K_UP):
            self.y_change += -self.y_dist
        elif (key == pygame.K_DOWN):
            self.y_change += self.y_dist

    def MoveKeyUp(self, key):
        """Responds to a key-up event and stops movement accordingly"""
        if (key == pygame.K_UP):
            self.y_change += self.y_dist
        elif (key == pygame.K_DOWN):
            self.y_change += -self.y_dist

    def update(self):
        """
        Moves the Ship while ensuring it stays in bounds
        """
        # Moves it relative to its current location.
        self.rect.move_ip(0, self.y_change)
        # If the Ship moves off the screen, put it back on.
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > window_height - self.height:
            self.rect.y = window_height - self.height


class Asteroid(Entity):
    """
    The Asteroid!  Moves around the screen.
    """
    def __init__(self, x, y, width, height):
        super(Asteroid, self).__init__(x, y, width, height)

        self.image = pygame.image.load("asteroid.png")

        self.x_direction = 5
        # Positive = down, negative = up
        # # Current speed.
        self.speed = 5
        self.sp=False

    def update(self):
        # Move the Asteroid!
        self.rect.x-=5
        # Keep the Asteroid in bounds, and make it bounce off the sides.

class AsteroidSP(Entity): #powerup
    """
    The Asteroid!  Moves around the screen.
    """
    def __init__(self, x, y, width, height):
        super(AsteroidSP, self).__init__(x, y, width, height)

        self.image = pygame.image.load("asteroidSP.png")

        self.x_direction = 5
        # Positive = down, negative = up
        # # Current speed.
        self.speed = 5
        self.sp=True

    def update(self):
        # Move the Asteroid!
        self.rect.x-=10
        # Keep the Asteroid in bounds, and make it bounce off the sides.

class Laser(Entity):
    """
    The Laser! Destroys Asteroids
    """
    def __init__(self,x, y, width, height):
        super(Laser, self).__init__(x, y, width, height)

        self.image = pygame.image.load("bullet.png")

        self.x_direction = 5
        # Positive = down, negative = up
        # # Current speed.
        self.speed = 5

    def update(self):
        # Move the Laser!
        self.rect.x+=5

#----------------------------------------------
#FUNCTIONS
#----------------------------------------------

def checkScreen(asteroids,lasers):
    global score
    for i in asteroids:
        if i.rect.x<=0:
            i.remove(all_sprites_list)
            asteroids.remove(i)
            if player.killed==False:
                score-=100
    for i in lasers:
        if i.rect.x>=window_width:
            i.remove(all_sprites_list)
            lasers.remove(i)

def checkKill(all):
    global lives
    for i in all:
        if player.killed==False:
            if doRectOverlap(i.rect,player.rect):
                all.remove(i)
                i.remove(all_sprites_list)
                lives-=1
                deathSound.play()
    if lives<=0: #only label them "killed" if they have no more lives
        player.killed=True

def laserHit(asteroids,lasers):
    global score
    for i in asteroids:
        for x in listLaser:
            if doRectOverlap(i.rect,x.rect):
                i.remove(all_sprites_list)
                x.remove(all_sprites_list)
                asteroids.remove(i)
                lasers.remove(x)
                if i.sp:
                    score+=1000
                else:
                    score+=100
                boomSound.play()

def calcHighScores():
    global highScores,counterHS,score
    if counterHS==0:
        counterHS+=1
        with open('highscore.txt') as f:
            hs = f.readlines()
        for i in hs:
            highScores.append(int(i.replace("\n", "")))
        highScores.append(score)
        highScores.sort(reverse=True)
        highScores.pop()
        f=open('highscore.txt','w')
        counterW=0
        for i in highScores:
            if counterW<10:
                f.write(str(i)+"\n")
                counterW+=1
            else:
                f.write(str(i))
        f.close()
        pygame.mixer.music.load('ponyIslandTrack11.wav')
        pygame.mixer.music.play(-1, 0.0)

#-----------------------------------------------------------

pygame.init()

window_width = 700
window_height = 400
screen = pygame.display.set_mode((window_width, window_height))
screen.blit(background,(0,0))
pygame.display.set_caption("Asteroids")

clock = pygame.time.Clock()

First = Asteroid(window_width, random.randint(0,window_height-50), 54, 50)
listAsteroid.append(First)
player = Player(20, window_height / 2, 53,50)

all_sprites_list.add(First)
all_sprites_list.add(player)

font=pygame.font.SysFont("freesansbold.ttf",50) #font for scoreboard
fontSmall=pygame.font.SysFont("freesansbold.ttf",35) #font for scoreboard

highScores=[]
counterHS=0
menuVar=True #if you're on the menu or not
topScore=0 #for high score on menu
asteroidCount=0 #for calculating powerup status

f=open('highscore.txt','r')
topScore=int(f.readline().replace("\n",""))
f.close()

deathSound=pygame.mixer.Sound('robloxDeathSound.wav')
laserSound=pygame.mixer.Sound('laser.wav')
boomSound=pygame.mixer.Sound('boom.wav')
pygame.mixer.music.load('rickAstleyShootingStars.wav')
pygame.mixer.music.play(-1, 0.0)

while True:
    if menuVar:
        all_sprites_list.remove(player)
        title1 = font.render("THAT ONE GAME WITH ASTEROIDS", 1, WHITE)
        title2 = font.render("AND YOU HAVE A SPACESHIP THAT", 1, WHITE)
        title3 = font.render("FIRES BULLETS THAT SCREAM 'LASER'", 1, WHITE)
        screen.blit(title1,(40,50))
        screen.blit(title2, (40, 80))
        screen.blit(title3, (10, 110))
        startInst=fontSmall.render("<Press SPACE to start the game>",1,WHITE) #game start instructions
        hsInst = fontSmall.render("High Score: {0}".format(topScore), 1, WHITE) #highest current score
        comInst = fontSmall.render("Controls: <UP> and <DOWN> to move, <SPACE> to shoot",1,WHITE) #controls
        screen.blit(startInst,(window_width/2-200,270))
        screen.blit(hsInst, (window_width/2-100,300))
        screen.blit(comInst,(window_width/2-335,370))
        # Event processing here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key==pygame.K_SPACE:
                menuVar=False
    elif menuVar==False:
        all_sprites_list.add(player)
        laserHit(listAsteroid,listLaser) #Check if laser hits asteroid
        checkKill(listAsteroid) #Check if player hit by asteroid
        checkScreen(listAsteroid,listLaser) #Check if anything off screen
        if not player.killed:
            asteroidCount+=1
            if creationTime<=0:#This creates asteroids after set amount of time
                if asteroidCount%17==0:
                    x = AsteroidSP(window_width - 1, random.randint(0, window_height - 50), 54, 50)
                else:
                    x=Asteroid(window_width-1, random.randint(0,window_height-50), 54, 50)
                listAsteroid.append(x)
                all_sprites_list.add(x)
                leveltime-=.25 #each time an asteroid is formed we make it shorter until next is made
                creationTime=leveltime
        # Event processing here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                player.MoveKeyDown(event.key)
            elif event.type == pygame.KEYUP:
                player.MoveKeyUp(event.key)

        for ent in all_sprites_list:
            ent.update()

        screen.blit(background,(0,0))

        if player.killed==False: #Only display score and lives if the player is still alive
            pTxt = font.render("Score: {0}".format(score), 1, WHITE)
            livesTxt = font.render("Lives: {0}".format(lives), 1, WHITE)
            screen.blit(pTxt, (100, 10))
            screen.blit(livesTxt, (450, 10))
        else: #otherwise, the player is removed from the game and given a game over screen
            calcHighScores()
            all_sprites_list.remove(player)
            overTxt=font.render("GAME OVER", 1, WHITE)
            pTxt = font.render("Your Score: {0}".format(score), 1, WHITE)
            screen.blit(overTxt,(window_width/2,10))
            screen.blit(pTxt, (window_width/2,40))
            #high scores
            hsTitle=font.render("HIGH SCORES:",1,WHITE)
            score1=font.render("1. {0}".format(highScores[0]),1,WHITE)
            score2 = font.render("2. {0}".format(highScores[1]), 1, WHITE)
            score3 = font.render("3. {0}".format(highScores[2]), 1, WHITE)
            score4 = font.render("4. {0}".format(highScores[3]), 1, WHITE)
            score5 = font.render("5. {0}".format(highScores[4]), 1, WHITE)
            score6 = font.render("6. {0}".format(highScores[5]), 1, WHITE)
            score7 = font.render("7. {0}".format(highScores[6]), 1, WHITE)
            score8 = font.render("8. {0}".format(highScores[7]), 1, WHITE)
            score9 = font.render("9. {0}".format(highScores[8]), 1, WHITE)
            score10 = font.render("10. {0}".format(highScores[9]), 1, WHITE)
            screen.blit(hsTitle,(10,10))
            screen.blit(score1, (10, 40))
            screen.blit(score2, (10, 70))
            screen.blit(score3, (10, 100))
            screen.blit(score4, (10, 130))
            screen.blit(score5, (10, 160))
            screen.blit(score6, (10, 190))
            screen.blit(score7, (10, 220))
            screen.blit(score8, (10, 250))
            screen.blit(score9, (10, 280))
            screen.blit(score10, (10, 310))

    all_sprites_list.draw(screen)
    creationTime-=1
    pygame.display.flip()

    clock.tick(60)