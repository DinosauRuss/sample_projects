
import pygame
import os
import sys
from random import randint


pygame.init()

width = 800
height = 600

os.environ['SDL_VIDEO_CENTERED'] = 'True'
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Space')

bg = pygame.image.load('/home/rek/Documents/python/sample_projects/stars.jpg')

clock = pygame.time.Clock()


class SpaceShip():
    
    def __init__(self):
        img = pygame.image.load('orangeship.png')
        shipSize = (img.get_rect().size)
        self.ship = pygame.transform.scale(img, (int(shipSize[0]/3), int(shipSize[1]/3)))
        shipRect = self.ship.get_rect()

        self.width = shipRect[2]
        self.height = shipRect[3]
        self.x = 0
        self.y = 0
        self.xSpeed = 0
        self.ySpeed = 0
        self.speedLimit = 20
        self.keys = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]

    def changeMoveKeys(self, upKey, downKey, leftKey, rightKey):
        # change movement keys if needed for second instance
        
        self.keys = [upKey, downKey, leftKey, rightKey]

    def moveKeys(self, keys):
        # arrow keys move rectangle around screen with momentum
        pressed = pygame.key.get_pressed()
        if pressed[self.keys[0]]: self.ySpeed -= 1
        if pressed[self.keys[1]]: self.ySpeed += 1
        if pressed[self.keys[2]]: self.xSpeed -= 1
        if pressed[self.keys[3]]: self.xSpeed += 1

        self.x += self.xSpeed
        self.y += self.ySpeed


    def teleportWall(self):
        '''object teleports through screen boundary'''
        
        screenWidth = pygame.display.set_mode().get_size()[0]
        screenHeight = pygame.display.set_mode().get_size()[1]

        if self.x <= (0-self.width):
            self.x = screenWidth-1
        if self.x >= screenWidth:
            self.x = (0-self.width)

        if self.y <= (0-self.height):
            self.y = screenHeight-1
        if self.y >= screenHeight:
            self.y = 0-self.height
        

    def checkWallX(self):
        '''object bounces off x boundary walls'''

        screenWidth = pygame.display.set_mode().get_size()[0]
        
        if self.x <= 0 or self.x >= (screenWidth-self.width):
            return (-1)
        else:
            return 1

    def checkWallY(self):
        '''object bounces off y boundary walls'''

        screenHeight = pygame.display.set_mode().get_size()[1]
        
        if self.y <= 0 or self.y >= (screenHeight-self.height):
            return (-1)
        else:
            return 1


    def maxSpeedX(self):
        '''x speed governor'''
        
        if self.xSpeed >= self.speedLimit:
            return self.speedLimit
        if self.xSpeed <= -self.speedLimit:
            return -self.speedLimit
        return self.xSpeed

    def maxSpeedY(self):
        '''y speed governor'''
        
        if self.ySpeed >= self.speedLimit:
            return self.speedLimit
        if self.ySpeed <= -self.speedLimit:
            return -self.speedLimit
        return self.ySpeed   


    def slowMomentum(self):
        '''Spacebar slows movement'''
        
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            print(self.xSpeed, self.ySpeed)
            if self.xSpeed < -5: self.xSpeed = -5
            if self.xSpeed > 5: self.xSpeed = 5
            if self.ySpeed < -5: self.ySpeed = -5
            if self.ySpeed > 5: self.ySpeed = 5


    def flyShip(self):
        # move with keys, check boundary, check speed limit
        self.moveKeys(self.keys)
        
##        self.xSpeed *= self.checkWallX()
##        self.ySpeed *= self.checkWallY()
        self.teleportWall()
        
        self.xSpeed = self.maxSpeedX()
        self.ySpeed = self.maxSpeedY()

        self.slowMomentum()
        
        

def waitForEsc():
    '''ESC button quits game'''

    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        print('Program quit')
        pygame.quit()
        sys.exit()


def gameLoop():

    bugs = SpaceShip()
    bugs.x = width/2
    bugs.y = height-bugs.height

    babs = SpaceShip()
    babs.x = width-babs.width
    babs.changeMoveKeys(pygame.K_e, pygame.K_d,\
                  pygame.K_s, pygame.K_f)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        #### print speed for debugging
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_m]: print(bugs.xSpeed, bugs.ySpeed)
        ####

        bugs.flyShip()
        babs.flyShip()
        
        screen.fill((0,0,0))
        screen.blit(bg, (0,0))
        screen.blit(bugs.ship, (bugs.x, bugs.y))
        screen.blit(babs.ship, (babs.x, babs.y))
        
        clock.tick(40)
        pygame.display.flip()

        waitForEsc()



if __name__ == '__main__':
    gameLoop()

    
