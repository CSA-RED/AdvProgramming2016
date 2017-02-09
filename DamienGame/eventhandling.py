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
Event Handling
2/3/2017
Adv. Comp. Prog.
Version 2
'''

import pygame, sys
from pygame.locals import *

pygame.init()

FPS = 15 # frames per second setting
fpsClock = pygame.time.Clock()

# set up the window
DISPLAYSURF = pygame.display.set_mode((600, 500))
pygame.display.set_caption('Event Handling')

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

#sprite
d=pygame.image.load('DamienSprite.png')
n=pygame.image.load('NighthawkSprite3.png')
dx=536
dy=380
nx=0
ny=168

#buttons
exitBtn=pygame.image.load('EXIT.png')
saveBtn=pygame.image.load('SAVE.png')
loadBtn=pygame.image.load('LOAD.png')
clickBtn=pygame.image.load('CLICK.png')

#audio
soundObj=pygame.mixer.Sound('starSound.wav')

#other variables
quitted=False
saved=False
loaded=False

# run the game loop
while True:
    DISPLAYSURF.fill(WHITE)
    pygame.draw.line(DISPLAYSURF, BLACK, (0, 65), (700, 65), 1)
    DISPLAYSURF.blit(exitBtn,(10,10))
    DISPLAYSURF.blit(loadBtn, (250, 10))
    DISPLAYSURF.blit(saveBtn,(490,10))
    mouseClicked=False
    buttonClicked=False
    play=False

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            mousex, mousey = event.pos
        elif event.type == MOUSEBUTTONDOWN:
            mousex, mousey = event.pos
            mouseClicked = True
        elif event.type==KEYDOWN:
            buttonClicked=True

    #event handling for button clicked
    if quitted:
        pygame.quit()
        sys.exit()
    elif saved:
        DISPLAYSURF.blit(clickBtn, (490, 10))
        f=open('location.txt','w')
        f.write(str(dx)+" "+(str(dy))+"\n")
        f.write(str(nx)+" "+(str(ny)))
        f.close()
        pygame.time.wait(100)
        saved=False
    elif loaded:
        DISPLAYSURF.blit(clickBtn, (250, 10))
        f=open('location.txt','r')
        points=f.readline().strip('\n').split()
        points2 = f.readline().split()
        f.close()
        dx=int(points[0])
        dy=int(points[1])
        nx=int(points2[0])
        ny=int(points2[1])
        pygame.time.wait(100)
        loaded=False

    #getting old positions
    oldDx=dx
    oldDy=dy
    oldNx=nx
    oldNy=ny

    #getting new positions
    if mouseClicked:
        dx,dy=mousex-32,mousey-60
        if mousey-60<=65:
            dy=66
        elif mousey-60>=381:
            dy=380
        if mousex-32>=537:
            dx=536
        elif mousex-32<=0:
            dx=0
        #check if button clicked
        if mousex>=10 and mousex<=110 and mousey>=10 and mousey<=60:
            DISPLAYSURF.blit(clickBtn,(10,10))
            quitted=True
            dx,dy=oldDx,oldDy
        elif mousex>=490 and mousex<=590 and mousey>=10 and mousey<=60:
            DISPLAYSURF.blit(clickBtn,(490,10))
            saved=True
            dx,dy=oldDx,oldDy
        elif  mousex>=250 and mousex<=350 and mousey>=10 and mousey<=60:
            DISPLAYSURF.blit(clickBtn, (250, 10))
            loaded=True
            dx,dy=oldDx,oldDy
        if quitted!=True and saved!=True and loaded!=True:
            soundObj.play()
    elif buttonClicked:
        #damien
        if event.key in (K_LEFT,K_j): #left
            dx,dy=oldDx-10,oldDy
            if dx<=0:
                dx=0
            play=True
        elif event.key in (K_RIGHT,K_l): #right
            dx, dy = oldDx +10, oldDy
            if dx>=537:
                dx=536
            play=True
        elif event.key in (K_UP,K_i): #up
            dx,dy=oldDx,oldDy-10
            if dy<=65:
                dy=66
            play=True
        elif event.key in (K_DOWN,K_k): #down
            dx,dy=oldDx,oldDy+10
            if dy>=381:
                dy=380
            play=True
        #nighthawk
        elif event.key in (K_a,): #left
            nx,ny=oldNx-10,oldNy
            if nx<=0:
                nx=0
            play=True
        elif event.key in (K_d,): #right
            nx, ny = oldNx +10, oldNy
            if nx>=351:
                nx=350
            play=True
        elif event.key in (K_w,): #up
            nx,ny=oldNx,oldNy-10
            if ny<=65:
                ny=66
            play=True
        elif event.key in (K_s,): #down
            nx,ny=oldNx,oldNy+10
            if ny>=169:
                ny=168
            play=True
        if play:
            soundObj.play()

    DISPLAYSURF.blit(n,(nx,ny))
    DISPLAYSURF.blit(d,(dx,dy))

    pygame.display.update()
