
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


class SpaceShip(pygame.sprite.Sprite):
    
    def __init__(self):
        
        super().__init__()
        
        img = pygame.image.load('orangeship.png')
        shipSize = (img.get_rect().size)
        self.ship = pygame.transform.scale(img, (int(shipSize[0]/3), int(shipSize[1]/3)))
        self.rect = self.ship.get_rect()

        self.width = self.rect.width
        self.height = self.rect.height
##        self.x = 0
##        self.y = 0
        self.xSpeed = 0
        self.ySpeed = 0
        self.speedLimit = 20
        self.keys = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]

    def setPosition(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def changeMoveKeys(self, upKey, downKey, leftKey, rightKey):
        # change movement keys if needed for second instance
        
        self.keys = [upKey, downKey, leftKey, rightKey]

    def moveKeys(self, keys):
        # arrow keys move rectangle around screen with momentum
        pressed = pygame.key.get_pressed()
        if pressed[self.keys[0]]: self.ySpeed -= 1 # up
        if pressed[self.keys[1]]: self.ySpeed += 1 #down
        if pressed[self.keys[2]]: self.xSpeed -= 1 #left
        if pressed[self.keys[3]]: self.xSpeed += 1 #right

        self.rect.x += self.xSpeed
        self.rect.y += self.ySpeed


    def teleportWall(self):
        '''ship teleports through screen boundary'''
        
        screenWidth = pygame.display.set_mode().get_size()[0]
        screenHeight = pygame.display.set_mode().get_size()[1]

        if self.rect.x <= (0-self.width):
            self.rect.x = screenWidth-1
        if self.rect.x >= screenWidth:
            self.rect.x = (0-self.width)

        if self.rect.y <= (0-self.height):
            self.rect.y = screenHeight-1
        if self.rect.y >= screenHeight:
            self.rect.y = 0-self.height
        

    def bounceWalls(self):
        '''ship bounces off screen boundary'''
        
        screenWidth = pygame.display.set_mode().get_size()[0]
        screenHeight = pygame.display.set_mode().get_size()[1]

        if self.rect.x <= 1 or self.rect.x > (screenWidth-self.width)-1:
            self.xSpeed *= -1
        if self.rect.y <= 0 or self.rect.y > (screenHeight-self.height):
            self.ySpeed *= -1


    def maxSpeed(self):
        '''speed governor'''
        
        if self.xSpeed >= self.speedLimit:
            self.xSpeed = self.speedLimit
        if self.xSpeed <= -self.speedLimit:
            self.xSpeed = -self.speedLimit

        if self.ySpeed >= self.speedLimit:
            self.ySpeed = self.speedLimit
        if self.ySpeed <= -self.speedLimit:
            self.ySpeed = -self.speedLimit


    def slowMomentum(self):
        '''Spacebar slows movement'''
        
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            print(self.xSpeed, self.ySpeed)
            if self.xSpeed < -5: self.xSpeed = -5
            if self.xSpeed > 5: self.xSpeed = 5
            if self.ySpeed < -5: self.ySpeed = -5
            if self.ySpeed > 5: self.ySpeed = 5


    def flyShip(self):
        '''move with keys, check boundary behavior, enforce speed limit'''
        
        self.moveKeys(self.keys)

        self.bounceWalls()
##        self.teleportWall()
        
        self.maxSpeed()
        self.slowMomentum()


    def rotateShip(self, angle):
        pass


def waitForEsc():
    '''ESC button quits game'''

    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        print('Program quit')
        pygame.quit()
        sys.exit()


def gameLoop():

    space_group = pygame.sprite.Group()
    
    bugs = SpaceShip()
    bugs.setPosition(width/2, height-bugs.height)

    babs = SpaceShip()
    babs.setPosition(0,0)
    babs.changeMoveKeys(pygame.K_e, pygame.K_d,\
                  pygame.K_s, pygame.K_f)

    space_group.add(bugs, babs)
    print(bugs.rect, babs.rect)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #### print speed for debugging
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    print(bugs.xSpeed, bugs.ySpeed)
            ####

        bugs.flyShip()
        babs.flyShip()
        
        if pygame.sprite.collide_rect(bugs, babs):
            print('Bunny', bugs.rect, babs.rect)

        screen.fill((0,0,0))
        screen.blit(bg, (0,0))
        screen.blit(bugs.ship, (bugs.rect.x, bugs.rect.y))
        screen.blit(babs.ship, (babs.rect.x, babs.rect.y))
        
        clock.tick(40)
        pygame.display.flip()

        waitForEsc()



if __name__ == '__main__':
    gameLoop()

    
