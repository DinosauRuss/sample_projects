'''
Program to create bound parent/child sprites
where the child sprites movement and rotation
is linked to its parent sprite.

Rotation can be controlled from keyboard or mouse input.
'''

import os
import pygame as pg
import sys
from math import *
vect = pg.math.Vector2

sWidth = 800
sHeight = 600

BLACK = (0,0,0)
BLUE  = (0,0,255)

FPS = 60

class Parent(pg.sprite.Sprite):
    def __init__(self, startx, starty):
        super().__init__()
        
        self.image = pg.Surface((75, 30))
        self.image.fill(BLUE)
        self.image.set_colorkey(BLACK)
        self.static_image = self.image
        self.rect = self.image.get_rect()
        self.rotatedDegree = 0
        self.rect.center = (startx, starty)
        
class Child(pg.sprite.Sprite):
    def __init__(self, parent, offset):
        super().__init__()
        
        self.image = pg.Surface((30,30))
        self.image.fill(BLUE)
        self.image.set_colorkey(BLACK)
        self.static_image = self.image
        self.rect = self.image.get_rect()
        
        self.parent = parent
        self.rotatedDegree = self.parent.rotatedDegree
        self.offset = offset
        self.rect.center = self.parent.rect.center + self.findNewPoint()
        
    def findNewPoint(self):
        x = cos(radians(self.offset[1]))*self.offset[0]
        y = sin(radians(self.offset[1]))*self.offset[0]
        return vect(x, -y)
    
    def update(self):
        if self.parent.rotatedDegree != self.rotatedDegree:
            parentDegreeChange = self.parent.rotatedDegree-self.rotatedDegree
            rotateImage(self, parentDegreeChange)
            self.offset.y += parentDegreeChange

        self.rect.center = self.parent.rect.center
        self.rect.center += self.findNewPoint()

        
class Game():
    def __init__(self, screen):
        self.program_running = True
        self.screen = screen
        self.clock = pg.time.Clock()
        
    def new(self):    
        # Create sprite groups
        self.all_sprites = pg.sprite.Group()
        
        #Create sprites
        self.fred = Parent(sWidth/2, sHeight/2)
        self.all_sprites.add(self.fred)

        self.pebbles = Child(self.fred, vect(100,20))
        self.all_sprites.add(self.pebbles)
        
        self.mouse_home = vect(self.fred.rect.center)
        self.mouse = vect(0,0)
        self.angleMouse = 0
        
        self.run()
        
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            self.waitForEsc()
        
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.program_running = False
        
        # Move Fred around        
        pressed = pg.key.get_pressed()
        if pressed[pg.K_c]:
            rotateImage(self.fred, 2)
        if pressed[pg.K_v]:
            rotateImage(self.fred, -2)
        
        if pressed[pg.K_UP]:
            self.fred.rect.y -= 5
        if pressed[pg.K_DOWN]:
            self.fred.rect.y += 5
        if pressed[pg.K_LEFT]:
            self.fred.rect.x-= 5
        if pressed[pg.K_RIGHT]:
            self.fred.rect.x += 5
        
        # Move Pebbles around in relation to Fred
        if pressed[pg.K_e]:
            self.pebbles.offset.x += 5
        if pressed[pg.K_d]:
            self.pebbles.offset.x -= 5
        if pressed[pg.K_s]:
            self.pebbles.offset.y += 5
        if pressed[pg.K_f]:
            self.pebbles.offset.y -= 5
            
        # Parent/child rotate as a group based on mouse position
        m = pg.mouse.get_pressed()
        if m[0] == True:
            self.mouse = vect(pg.mouse.get_pos())
            self.findMouseAngle()
            rotateImage(self.fred, self.angleMouse-self.fred.rotatedDegree)
    
    def update(self):
        # run all sprites update functions
        self.all_sprites.update()
        self.mouse_home = vect(self.fred.rect.center)
        
    def draw(self):
        #draw graphics
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def findMouseAngle(self):
        xy = self.mouse - self.mouse_home
        self.angleMouse = degrees(atan2(radians(-xy.y), radians(xy.x)))

    def waitForEsc(self):
        pressed = pg.key.get_pressed()
        if pressed[pg.K_ESCAPE]:
            self.playing = False
            self.program_running = False


def rotateImage(sprite, angle):
        '''rotates image in place around center'''
        
        currentPos = sprite.rect.center # point to rotate around
        
        degree = (sprite.rotatedDegree + angle)
        sprite.rotatedDegree = degree #keep track of rotation angle
        sprite.rotatedDegree %= 360

        # rotate unmodified ship image
        sprite.image = pg.transform.rotate(sprite.static_image, degree)
        
        sprite.rect = sprite.image.get_rect() #update rect property
        sprite.rect.center = currentPos #reset position to original position

def mainLoop():
    pg.init()
    os.environ['SDL_VIDEO_CENTERED'] = 'True'
    screen = pg.display.set_mode((sWidth, sHeight))
    pg.display.set_caption('Gravity')
    
    game = Game(screen)
    while game.program_running:
        game.new()

    pg.quit()
    sys.exit()
    

if __name__ == '__main__':
    mainLoop()

