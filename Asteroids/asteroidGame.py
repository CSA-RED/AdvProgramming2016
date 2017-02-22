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
2/17/2017
Adv. Comp. Prog.
Version 1
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
            x = Laser(player.rect.x + 20, player.rect.y + 18, 46, 15)
            all_sprites_list.add(x)
            listLaser.append(x)
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

    def update(self):
        # Move the Asteroid!
        self.rect.x-=5
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
        if doRectOverlap(i.rect,player.rect):
            all.remove(i)
            i.remove(all_sprites_list)
            lives-=1
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
                score+=100

#-----------------------------------------------------------

pygame.init()

window_width = 700
window_height = 400
screen = pygame.display.set_mode((window_width, window_height))
screen.blit(background,(0,0))
pygame.display.set_caption("Asteroids")

clock = pygame.time.Clock()

First = Asteroid(window_width, random.randint(10,window_height-10), 54, 50)
listAsteroid.append(First)
player = Player(20, window_height / 2, 40, 37)

all_sprites_list.add(First)
all_sprites_list.add(player)

font=pygame.font.SysFont("freesansbold.ttf",50) #font for scoreboard

while True:
    laserHit(listAsteroid,listLaser) #Check if laser hits asteroid
    checkKill(listAsteroid) #Check if player hit by asteroid
    checkScreen(listAsteroid,listLaser) #Check if anything off screen
    if creationTime<=0:#This creates asteroids after set amount of time
        x=Asteroid(window_width-1, random.randint(0,window_height-20), 54, 50)
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
        all_sprites_list.remove(player)
        overTxt=font.render("GAME OVER", 1, WHITE)
        pTxt = font.render("Final Score: {0}".format(score), 1, WHITE)
        screen.blit(overTxt,(window_width/2,window_height/2))
        screen.blit(pTxt, (window_width/2,(window_height/2)+30))

    all_sprites_list.draw(screen)
    creationTime-=1
    pygame.display.flip()

    clock.tick(60)