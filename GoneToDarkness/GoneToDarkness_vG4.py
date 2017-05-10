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
Gone to Darkness
5/5/2017
Adv. Comp. Prog.
Version 1.4
'''

import pygame, sys, random
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock() #for sprite updates
FPS=30

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

background=pygame.image.load("DungeonBack2.png")

#CLASSES#####

class Option(): #credit to Josh Hinojosa for helping with the mouse hovering code
    def __init__(self, text, x, y):
        self.text=text
        self.x=x
        self.y=y
        self.hovered=False
        self.update()
    def getcolor(self):
        if self.hovered:
            return (255,255,255)
        else:
            return (0,0,0)
    def set_rect(self):
        self.rend = font.render(self.text, True, self.getcolor())
        self.rect = self.rend.get_rect()
        self.rect.topleft = (self.x,self.y)
    def update(self):
        self.set_rect()
        screen.blit(self.rend,self.rect)

class OptionB(): #credit to Josh Hinojosa for helping with the mouse hovering code
    def __init__(self, text, x, y):
        self.text=text
        self.x=x
        self.y=y
        self.hovered=False
        self.update()
    def getcolor(self):
        if self.hovered:
            return (255,255,255)
        else:
            return (0,0,0)
    def set_rect(self):
        self.rend = font2.render(self.text, True, self.getcolor())
        self.rect = self.rend.get_rect()
        self.rect.topleft = (self.x,self.y)
    def update(self):
        self.set_rect()
        screen.blit(self.rend,self.rect)

class Text():
    def __init__(self, text, x, y):
        self.text=text
        self.x=x
        self.y=y
        self.update()
    def set_rect(self):
        self.rend = font.render(self.text, True, (255,255,255))
        self.rect = self.rend.get_rect()
        self.rect.topleft = (self.x,self.y)
    def update(self):
        self.set_rect()
        screen.blit(self.rend,self.rect)

class TextB():
    def __init__(self, text, x, y):
        self.text=text
        self.x=x
        self.y=y
        self.update()
    def set_rect(self):
        self.rend = font2.render(self.text, True, (255,255,255))
        self.rect = self.rend.get_rect()
        self.rect.topleft = (self.x,self.y)
    def update(self):
        self.set_rect()
        screen.blit(self.rend,self.rect)

#################################################################################
# The reason for A and B classes is because dynamic font settings wouldn't work #
#################################################################################

class Entity():
    def __init__(self,x, y, width, height,sprite):
        # computational points
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)  # for collisions
        self.image = pygame.image.load(sprite)
    def update(self):
        self.rect.x=self.x
        self.rect.y=self.y
        screen.blit(self.image, (self.x, self.y))

class Fighter():
    def __init__(self, hp, max_hp, attack, defense, magic, name, x, y, width, height, hero,images):
        #stats
        self.hp = hp
        self.max_hp = max_hp
        self.attack = attack
        self.defense = defense
        self.magic = magic
        self.name=name
        self.nameU=self.name.upper()
        #computational points
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height) #for collisions
        self.images=images
        self.image=None
        self.hero=hero
        self.index=0
        self.animation_time = 0.3
        self.current_time = 0
        if self.hero:
            self.nameDisplay = TextB(self.nameU, 180, 367)
        else:
            self.nameDisplay=TextB(self.nameU,15,367)
    def spriteUpdate(self,dt):
        #animation update
        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images)
        self.image = self.images[self.index]
    def update(self,dt):
        #screen update
        if self.hero:
            self.healthDisplay=Text(str(self.hp)+"/"+str(self.max_hp),180,427)
        else:
            self.healthDisplay = Text(str(self.hp) + "/" + str(self.max_hp), 15, 427)
        self.spriteUpdate(dt)
        self.image=pygame.image.load(self.image)
        screen.blit(self.image,(self.x,self.y))
        self.nameDisplay.update()
        self.healthDisplay.update()

#FUNCTIONS#####

damageTotal=0
counterPF=0

counterAnim=0
hit=False

#-Attack Animation
def pAttackAnim(enemy):
    global counterAnim,hit,allSprites,arrow
    arrow.x=538
    arrow.y=d.y
    allSprites.append(arrow)
    if counterAnim==0:
        arrowSound.play()
    if not arrow.rect.colliderect(enemy.rect):
        arrow.x-=counterAnim*10
        counterAnim+=1
    if arrow.rect.colliderect(enemy.rect):
        arrow.x=999
        hit=True

def pMagicAnim(enemy):
    global counterAnim,fBall,hit,allSprites
    fBall.x=488
    fBall.y=d.y
    allSprites.append(fBall)
    if counterAnim==0:
        magicSound.play()
    if not fBall.rect.colliderect(enemy.rect):
        fBall.x-=counterAnim*10
        counterAnim+=1
    if fBall.rect.colliderect(enemy.rect):
        fBall.x=999
        hit=True

#-Game functions
def playerFight(enemy): #if the fight option is chosen
    global allText,damageTotal
    damageTotal = random.randint(3,5)
    displayU=TextB(d.nameU+" DEALT ",window_width/2+30,367)
    displayU2=TextB(str(damageTotal)+" DAMAGE",window_width/2+30,397)
    displayU3=TextB("TO "+enemy.nameU+"!",window_width/2+30,427)
    enemy.hp-=damageTotal
    if enemy.hp<0:
        enemy.hp=0
    allText.append(displayU)
    allText.append(displayU2)
    allText.append(displayU3)

def enemyFight(enemy): #if enemy performs a normal attack
    global allText, damageTotal
    damageTotal = random.randint(3,8)
    displayU = TextB(enemy.nameU + " DEALT ", window_width / 2 + 30, 367)
    displayU2 = TextB(str(damageTotal) + " DAMAGE", window_width / 2 + 30, 397)
    displayU3 = TextB("TO " + d.nameU + "!", window_width / 2 + 30, 427)
    d.hp -= damageTotal
    if d.hp<0:
        d.hp=0
    allText.append(displayU)
    allText.append(displayU2)
    allText.append(displayU3)

def playerMagic(enemy): #if the magic option is chosen
    global allText, damageTotal
    damageTotal = random.randint(1,7)
    displayU = TextB(d.nameU + " DEALT ", window_width / 2 + 30, 367)
    displayU2=TextB(str(damageTotal) + " DAMAGE",window_width/2+30,397)
    displayU3 = TextB("TO " + enemy.nameU + "!", window_width / 2 + 30, 427)
    enemy.hp -= damageTotal
    if enemy.hp<0:
        enemy.hp=0
    allText.append(displayU)
    allText.append(displayU2)
    allText.append(displayU3)

def enemyMagic(enemy): #if enemy performs a magic attack
    global allText, damageTotal
    damageTotal = random.randint(3,8)
    displayU = TextB(enemy.nameU + " DEALT ", window_width / 2 + 30, 367)
    displayU2 = TextB(str(damageTotal) + " DAMAGE", window_width / 2 + 30, 397)
    displayU3 = TextB("TO " + d.nameU + "!", window_width / 2 + 30, 427)
    d.hp -= damageTotal
    if d.hp<0:
        d.hp=0
    allText.append(displayU)
    allText.append(displayU2)
    allText.append(displayU3)

def enemyRand(enemy):
    choice=random.randint(1,2)
    if choice==1:
        enemyFight(enemy)
    elif choice==2:
        enemyMagic(enemy)

#-Code functions
def clearAll(): #most clear functions for debugging
    global allOptions, allSprites, allText
    allSprites = []
    allOptions = []
    allText = []

def clearOptions():
    global allOptions
    allOptions = []

def clearSprites():
    global allSprites
    allSprites = []

def clearText():
    global allText
    allText = []

def defaultSprites(): #the default list used every time
    global allOptions,allSprites,allText
    allSprites = []
    allOptions = []
    allText = []
    allOptions.append(fight)
    allOptions.append(magic)
    allOptions.append(item)
    allOptions.append(shield)
    allSprites.append(msgBox)
    allSprites.append(msgBox2)
    allSprites.append(msgBox3)
    allSprites.append(d)
    allSprites.append(n)

def noMenu():
    global allSprites
    allSprites = []
    allSprites.append(d)
    allSprites.append(n)
    allSprites.append(msgBox)

def playerWin(enemy):
    global fightCounter,allText
    fightCounter=0
    enemy.x,enemy.y=999,999
    wTxt = TextB("CONGRATULATIONS!", window_width / 2 + 30, 367)
    wTxt2=TextB("DAMIEN DEFEATED",window_width/2+30,397)
    wTxt3 = TextB(enemy.nameU + "!", window_width/2+30,427)
    allText.append(wTxt)
    allText.append(wTxt2)
    allText.append(wTxt3)
    allSprites.append(msgBox4)
    allOptions.append(restart)
    allOptions.append(run)

def enemyWin(enemy):
    global fightCounter,allText
    fightCounter = 0
    d.x,d.y=999,999
    wTxt = TextB("DAMIEN WAS", window_width/2+30,367)
    wTxt2 = TextB("DEFEATED BY", window_width / 2 + 30, 397)
    wTxt3 = TextB(enemy.nameU+"...", window_width/2+30,427)
    allText.append(wTxt)
    allText.append(wTxt2)
    allText.append(wTxt3)
    allSprites.append(msgBox4)
    allOptions.append(restart)
    allOptions.append(run)

def restartF(enemy):
    global restartV,eWin,pWin,inventory
    eWin=False
    pWin=False
    enemy.x, enemy.y = 6, 10
    d.x, d.y = 570,222
    enemy.hp=enemy.max_hp
    d.hp=d.max_hp
    inventory = ["Lemonade", "Lemonade"]
    restartV=False

#Inventory Option

itmV=False
waitV=False

def invItems():
    global inventory,itmV,itemV,waitV,allText
    if itmV==False:
        if inventory.count("Lemonade") > 0:
            item=Option("LEMONADE x"+str(inventory.count("Lemonade")),window_width/2+30,367)
            exit=OptionB("<= [EXIT]",window_width/2+194,427)
            allOptions.append(item)
            allOptions.append(exit)
            for i in allOptions:
                if i.rect.collidepoint(pygame.mouse.get_pos()):
                    i.hovered = True
                else:
                    i.hovered = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if item.hovered:
                        allOptions.remove(item)
                        itmV=True
                    elif exit.hovered:
                        itemV=False
                        itmV=False
                        waitV=False
        else:
            usedMsg = TextB("NO REMAINING ITEMS!", window_width / 2 + 30, 367)
            allText.append(usedMsg)
            itemV = False
            itmV = False
            waitV = True
    else:
        usedMsg=TextB("DAMIEN USED ONE",window_width / 2 + 30, 367)
        usedMsg2 = TextB("LEMONADE! RESTORED", window_width/2+30,397)
        usedMsg3 = TextB("6 HP!", window_width/2+30,427)
        allText.append(usedMsg)
        allText.append(usedMsg2)
        allText.append(usedMsg3)
        d.hp+=6
        if d.hp>d.max_hp:
            d.hp=d.max_hp
        inventory.remove("Lemonade")
        itemV = False
        itmV = False
        waitV=True

#INITIATE#####

pygame.init()

window_width = 640
window_height = 480
screen = pygame.display.set_mode((window_width, window_height))
screen.blit(background,(0,0))
pygame.display.set_caption("Gone To Darkness")
font=pygame.font.SysFont("freesansbold.ttf",50)
font2=pygame.font.SysFont("freesansbold.ttf",30)

#Fighters
d=Fighter(20,20,9,5,8,"Damien",570,222,64,120,True,["DamienSprite-2.png","DamienSprite.png"])
n=Fighter(30,30,10,5,9,"Nighthawk",6,10,250,332,False,["NighthawkSprite3.png","NighthawkSprite3-2.png"])

#Fight Objects
arrow=Entity(538,d.y,32,10,"Arrow2.png")
fBall = Entity(488, d.y, 82, 50, "MaggyksBig.png")
fBall2 = Entity(n.x+n.width, d.y, 82, 50, "MaggyksBigE.png")

#Text Options
allOptions=[]
fight=Option("FIGHT",window_width/2+30,367)
magic=Option("MAGIC",window_width/2+30,427)
item=Option("ITEM",window_width/2+177,367)
shield=Option("RUN",window_width/2+177,427)
restart=Option("RESTART",window_width/2+30,19)
run=Option("EXIT",window_width/2+30,79)

#Visual objects
msgBox=Entity(0,348,640,132,"ChoiceMenu1.png")
msgBox2=Entity(163,348,314,132,"ChoiceMenu2.png")
msgBox3=Entity(326,348,314,132,"ChoiceMenu2.png")
msgBox4=Entity(326,0,314,132,"ChoiceMenu2.png")

#All sprites (for rendition iteration)
allSprites=[]
allText=[]

#Player inventory
inventory=["Lemonade","Lemonade"]

#flag variables
fightV=False
magicV=False
itemV=False
shieldV=False
restartV=False
runV=False

fightCounter=0 #used in loop to determine turns
pWin=False
eWin=False

#Music
arrowSound=pygame.mixer.Sound('arrowHit01.wav')
magicSound=pygame.mixer.Sound('Fire.aif')
pygame.mixer.music.load('Heroic Demise.mp3')
pygame.mixer.music.play(-1, 0.0)

while True:
    dt = clock.tick(FPS) / 1000
    defaultSprites()
    if runV:
        pygame.quit()
        sys.exit()
    elif restartV:
        restartF(n)
    elif fightV: #if/elif list used for checking what button was pressed
        clearOptions()
        if fightCounter==0:
            pAttackAnim(n)
            if hit==True:
                playerFight(n)
                counterAnim=0
                hit=False
                fightCounter += 1
            if n.hp<=0: #fix to accomodate any enemy
                fightV=False
                pWin=True
        elif fightCounter==1:
            enemyRand(n)
            if d.hp<=0:
                fightV=False
                eWin=True
            fightCounter += 1
        else:
            fightV=False
            fightCounter += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    elif magicV:
        clearOptions()
        if fightCounter==0:
            pMagicAnim(n)
            if hit==True:
                playerMagic(n)
                counterAnim=0
                hit=False
                fightCounter += 1
            if n.hp<=0: #fix to accomodate any enemy
                magicV=False
                pWin=True
        elif fightCounter==1:
            enemyRand(n)
            if d.hp<=0:
                magicV=False
                eWin=True
            fightCounter += 1
        else:
            magicV=False
            fightCounter += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    elif itemV:
        clearOptions()
        invItems()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    elif shieldV:
        clearOptions()
        usedMsg = TextB("DAMIEN ESCAPED!", window_width / 2 + 30, 367)
        allText.append(usedMsg)
        fightCounter+=1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    elif pWin:
        clearOptions()
        clearText()
        playerWin(n)
        for i in allOptions:
            if i.rect.collidepoint(pygame.mouse.get_pos()):
                i.hovered = True
            else:
                i.hovered = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if restart.hovered:
                    restartV=True
                elif run.hovered:
                    runV=True
    elif eWin:
        clearOptions()
        clearText()
        enemyWin(n)
        for i in allOptions:
            if i.rect.collidepoint(pygame.mouse.get_pos()):
                i.hovered = True
            else:
                i.hovered = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if restart.hovered:
                    restartV=True
                elif run.hovered:
                    runV=True
    else:
        for i in allOptions:
            if i.rect.collidepoint(pygame.mouse.get_pos()):
                i.hovered = True
            else:
                i.hovered = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if fight.hovered:
                    fightV=True
                    counterPF=0
                    fightCounter=0
                elif magic.hovered:
                    magicV=True
                    counterPF=0
                    fightCounter=0
                elif item.hovered:
                    itemV=True
                elif shield.hovered:
                    shieldV=True
                    fightCounter=0

    screen.blit(background, (0, 0))
    for i in allSprites:
        if type(i) is Fighter:
            i.update(dt)
        else:
            i.update()
    for i in allOptions:
        i.update()
    for i in allText:
        i.update()
    pygame.display.flip()
    if fightCounter==1 or fightCounter==2:
        pygame.time.wait(1500)
        if shieldV:
            pygame.quit()
            sys.exit()
    if waitV:
        pygame.time.wait(1500)
        waitV=False
