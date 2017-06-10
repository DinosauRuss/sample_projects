
'''
Program to test aspects of Pygame. Generate a rectangle of random
size, color, and location; can be moved with arrow keys and
respawned with spacebar.
'''

import pygame
from random import randint
import sys


pygame.init()

width = 600
height = 400

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Mac and Cheetos')

clock = pygame.time.Clock()

# start rectangle as grey, random size, ranodom location
color = (148,148,148)
x = randint(0, (width-50))
y = randint(0, (height-50))
size_x = randint(10,50)
size_y = randint(10,50)

rand_color = lambda: (randint(0,255), randint(0,255), randint(0,255))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        # spacebar randomly changes size,
        # color, and position of rectangle
        if event.type == pygame.KEYDOWN and\
           event.key == pygame.K_SPACE:
            color = rand_color()
            x = randint(0, width)
            y = randint(0, height)
            size_x = randint(10,50)
            size_y = randint(10,50)

    # arrow keys move rectangle around screen
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]: y -= 5
    if pressed[pygame.K_DOWN]: y += 5
    if pressed[pygame.K_LEFT]: x -= 5
    if pressed[pygame.K_RIGHT]: x += 5

    # keep rectangle within screen bounds
    if x<=0: x=0
    if y<=0: y=0
    if x>= width-size_x: x= width-size_x
    if y>= height-size_y: y= height-size_y
    
    screen.fill((0,0,0))
    pygame.draw.rect(screen, color, pygame.Rect(x,y, size_x, size_y))

    clock.tick(60)
    pygame.display.flip()


