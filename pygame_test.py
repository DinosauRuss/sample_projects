
'''
Program to test aspects of Pygame. Rectangle can be moved with arrow keys,
transport through screen boundaries, and has momentum.
'''

import pygame
import os
import sys
from random import randint


pygame.init()

width = 800
height = 600

os.environ['SDL_VIDEO_CENTERED'] = '1'
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Physics')

bg = pygame.image.load('stars.jpg')
clock = pygame.time.Clock()

# start rectangle as grey, random size, random location
color = (168,148,148)
size_x = randint(10,50)
size_y = randint(10,50)
x = randint(0, (width-50))
y = randint(0, (height-50))

xSpeed = 0
ySpeed = 0


def waitForEsc():
    '''ESC button quits game'''
    
    if pressed[pygame.K_ESCAPE]:
        print('Program quit')
        pygame.quit()
        sys.exit()

def slowMomentum():
    '''Spacebar slows movement'''
    
    global xSpeed, ySpeed
    if pressed[pygame.K_SPACE]:
        print(xSpeed, ySpeed)
        if xSpeed < -5: xSpeed = -5
        if xSpeed > 5: xSpeed = 5
        if ySpeed < -5: ySpeed = -5
        if ySpeed > 5: ySpeed = 5

def maxSpeed():
    '''speed governor'''
    
    global xSpeed, ySpeed
    if xSpeed > 20: xSpeed = 20
    if xSpeed < -20: xSpeed = -20
    if ySpeed > 20: ySpeed = 20
    if ySpeed < -20: ySpeed = -20


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    # arrow keys move rectangle around screen with momentum
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]: ySpeed -= .5
    if pressed[pygame.K_DOWN]: ySpeed += .5
    if pressed[pygame.K_LEFT]: xSpeed -= .5
    if pressed[pygame.K_RIGHT]: xSpeed += .5
    

    # transport rectangle through boundary to other side
    if x < 0-size_x: x=width
    if y < 0-size_y: y=height
    if x > width: x= 0
    if y > height: y= 0

    y += ySpeed
    x += xSpeed
    maxSpeed()

    slowMomentum()
    waitForEsc()
    
    screen.fill((0,0,0))
    screen.blit(bg, [0,0])
    pygame.draw.rect(screen, color, pygame.Rect(x,y, size_x, size_y))
    
    clock.tick(40)
    pygame.display.flip()
    


