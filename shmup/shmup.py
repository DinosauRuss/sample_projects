
'''
Python/Pygame program.
Emphasis is on logic and programming rather
than graphic design.
'''


import os
import pygame
import random
import sys


# screen size
sWidth = 400
sHeight = 600
fps = 60

# color variables
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
GREY = (148,148,148)
GOLD = (255, 215, 0)


pygame.init()
pygame.mixer.init()
os.environ['SDL_VIDEO_CENTERED'] = 'True'
screen = pygame.display.set_mode((sWidth, sHeight))
pygame.display.set_caption('Shmup Test')

clock = pygame.time.Clock()
font_name = pygame.font.match_font('verdana')

# folder locations
img_dir = os.path.join(os.path.dirname(__file__), 'images')
snd_dir = os.path.join(os.path.dirname(__file__), 'sounds')

# load game graphics
bg = pygame.image.load(os.path.join(\
    img_dir, 'sky.png')).convert_alpha()
player_img = pygame.image.load(os.path.join(\
    img_dir, 'tree.png')).convert_alpha()
apple_img = pygame.image.load(os.path.join(\
    img_dir, 'apple.png')).convert_alpha()

enemy_list = []
enemy_files = ['shipBeige.png', 'shipGreen.png',
               'shipPink.png', 'shipYellow.png']
for file in enemy_files:
    enemy_list.append(pygame.image.load(\
        os.path.join(img_dir, file)).convert_alpha())

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(os.path.join(\
        img_dir, filename)).convert_alpha()
    img_lg = pygame.transform.scale(img, (75,75))
    img_sm = pygame.transform.scale(img, (32,32))
    explosion_anim['lg'].append(img_lg)
    explosion_anim['sm'].append(img_sm)
    filename2 = 'sonicExplosion0{}.png'.format(i)
    img2 = pygame.image.load(os.path.join(\
        img_dir, filename2)).convert_alpha()
    img_sonic = pygame.transform.scale(img2, (150,150))
    explosion_anim['player'].append(img_sonic)

img_mini = pygame.transform.scale(player_img, (30,43)).convert_alpha()
img_mini_rect = img_mini.get_rect()

shield_img = pygame.image.load(\
    os.path.join(img_dir, 'Heart.png')).convert_alpha()
throw_img = pygame.image.load(\
    os.path.join(img_dir, 'Bolt.png')).convert_alpha()
bad_img = pygame.image.load(\
    os.path.join(img_dir, 'BadCloud.png')).convert_alpha()
bad_img = pygame.transform.scale(bad_img, (30, 20))

pow_images = {}
pow_images['shield'] = shield_img
pow_images['throw'] = throw_img
pow_images['bad'] = bad_img

# load game sounds
teleportSound = pygame.mixer.Sound(os.path.join(snd_dir, 'Pop.ogg'))
teleportSound.set_volume(.5)
pygame.mixer.music.load(os.path.join(snd_dir,\
            'Grassy World - Main Title Theme.mp3'))
pygame.mixer.music.set_volume(.1)


class Player(pygame.sprite.Sprite):

    def __init__(self, image=None, maxSize=30):
        super().__init__()

        # impor/resize image or basic shape placeholder
        if image != None:
            imgRect = image.get_rect().size
            if imgRect[0] > maxSize:
                self.image = \
                    pygame.transform.scale(image,\
                        (maxSize, int((maxSize*imgRect[1])/imgRect[0])))
                self.rect = self.image.get_rect()
        else:
            self.image = pygame.Surface((maxSize,maxSize))
            self.image.fill(RED)
            self.rect = self.image.get_rect()

        self.radius = int(self.rect.width/2)
##        pygame.draw.circle(self.image,\
##            GREY, self.rect.center, self.radius)
        self.rect.centerx = sWidth/2
        self.rect.bottom = sHeight - 10
        self.xSpeed = 0
        self.ySpeed = 0
        self.active = True
        self.shield = 100
        self.throwDelay = 350
        self.lastThrown = 0
        self.lives = 3
        self.hidden = False
        self.hideTimer = 0
        self.powerLevel = 1
        self.powerLevelTime = 0

    def move(self, speed=8):
        if self.active == True:
            # only move if key is pressed
            self.xSpeed = 0
            
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:
                self.xSpeed = -speed
            if pressed[pygame.K_RIGHT]:
                self.xSpeed = speed
            
            self.rect.x += self.xSpeed

    def boundary(self):
        # stay within screen bounds
        if self.rect.right > sWidth:
            self.rect.right = sWidth
        if self.rect.left < 0:
            self.rect.left = 0

    def throw(self, image, *args):
        # args are groups sprite needs to join
        if self.active == True:
            now = pygame.time.get_ticks()
            if now - self.lastThrown > self.throwDelay:
                self.lastThrown = now
                if self.powerLevel == 1:
                    Abe = Apple(self.rect.centerx, self.rect.top, image)
                    for i in args:
                        i.add(Abe)
                        # play some sound
                if self.powerLevel >= 2:
                    Abe = Apple(self.rect.centerx, self.rect.top, image)
                    George = Apple(self.rect.centerx, self.rect.top, image)
                    Tom = Apple(self.rect.centerx, self.rect.top, image)
                    George.xSpeed = -2
                    Tom.xSpeed = 2
                    for i in args:
                        i.add(Abe)
                        i.add(George)
                        i.add(Tom)
                        # play some sound
                
            
    def powerThrow(self):
        # set powerup level and time
        # executed in self.update
        self.powerLevel += 1
        self.powerLevelTime = pygame.time.get_ticks()
    
    def hide(self):
        # hide the player temporarily
        self.active = False
        self.hideTimer = pygame.time.get_ticks()
        self.hidden = True
        self.rect.y = sHeight + 100

    def update(self):
        
        # unhide if hidden
        if self.hidden == True and \
            pygame.time.get_ticks() - self.hideTimer > 3000:
            self.hidden = False
            self.active = True
            self.rect.bottom = sHeight - 10
            
        # reset powerthrow after some time
        now = pygame.time.get_ticks()
        if self.powerLevel >= 2 and now - self.powerLevelTime > 5000:
            self.powerLevel -= 1
        self.move()
        self.boundary()
        

class Mob(pygame.sprite.Sprite):

    def __init__(self, image=None, maxSize=50):
        super().__init__()

        maxSize = random.randrange(30,61,10)
        
        # import, shrink image or basic shape
        if image != None:
            imgRect = image.get_rect().size
            if imgRect[0] > maxSize:
                self.staticImage = \
                    pygame.transform.scale(image,\
                        (maxSize, int((maxSize*imgRect[1])/imgRect[0])))
            self.image = self.staticImage.copy()
            self.rect = self.image.get_rect()
        else:
            self.image = pygame.Surface((maxSize,maxSize))
            self.image.fill(RED)
            self.rect = self.image.get_rect()

        self.radius = int((self.rect.width)/2)
##        pygame.draw.circle(self.image,\
##        GOLD, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, sWidth-self.rect.width)
        self.rect.bottom = random.randrange(-50, -10)

        self.xSpeed = random.choice((0, random.randint(-1,1)))
        self.ySpeed = random.randrange(1,6)
        self.rotatedDegree = 0
        self.rotSpeed = random.randint(-4,4)
        self.lastUpdate = pygame.time.get_ticks()

    def move(self):
        self.rect.y += self.ySpeed
        self.rect.x += self.xSpeed

        # respawn if off the screen
        if (self.rect.top > sHeight+10) or\
               (self.rect.right < -5) or\
               (self.rect.x > sWidth+5):
            self.rect.x = random.randrange(0, sWidth-self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.ySpeed = random.randrange(1,6)
            self.xSpeed = random.choice((0, random.randint(-1,1)))        

    def rotate(self):
        # give mobs some animation when invading
        now = pygame.time.get_ticks()
        current_pos = self.rect.center

        # if 50 milliseconds have passed
        if now - self.lastUpdate > 50:
            self.lastUpdate = now

            # how far to rotate
            self.rotatedDegree += self.rotSpeed
            self.rotatedDegree %= 360

            # keep mobs upright but wobbling
            if 15 < self.rotatedDegree < 345:
                self.rotSpeed *= -1

            # rotate unmodified image
            self.image = pygame.transform.rotate(self.staticImage, self.rotatedDegree)
            self.rect = self.image.get_rect() # update rect
            self.rect.center = current_pos # reset position to original           

    def update(self):
        self.move()
        self.rotate()


class Apple(pygame.sprite.Sprite):

    def __init__(self, x, y, image=None, maxSize=10):
        super().__init__()

        # import, shrink image or basic shape
        if image != None:
            self.image = image
            imgRect = self.image.get_rect().size
            if imgRect[0] > maxSize:
                self.image = \
                    pygame.transform.scale(self.image,\
                        (maxSize, int((maxSize*imgRect[1])/imgRect[0])))
                self.rect = self.image.get_rect()
        else:
            self.image = pygame.Surface((maxSize,maxSize))
            self.image.fill(RED)
            self.rect = self.image.get_rect()

        self.radius = int((self.rect.width*.9)/2)
##        pygame.draw.circle(self.image,\
##        GOLD, self.rect.center, self.radius)
        self.rect.centerx = x
        self.rect.bottom = y

        self.xSpeed = 0
        self.ySpeed = -5

    def move(self):
        # moves upward on screen
        self.rect.y += self.ySpeed
        self.rect.x += self.xSpeed
        if self.rect.bottom < 0:
            self.kill()

    def update(self):
        self.move()


class Explosion(pygame.sprite.Sprite):
    
    def __init__(self, center, size):
        super().__init__()
        
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = 0
        self.frameRate = 25
    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frameRate:
            self.frame += 1
            self.last_update = now
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                currentPos = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = currentPos
            

class Powerup(pygame.sprite.Sprite):
    
    def __init__(self, center):
        super().__init__()
        
        self.option = random.choice(('shield', 'throw', 'bad'))
        self.image = pow_images[self.option]
        self.rect = self.image.get_rect()
        self.rect.center = center
        if self.option == 'bad':
            self.ySpeed = 3
        else:
            self.ySpeed = 6
    
    def update(self):
        self.rect.y += self.ySpeed
        # remove if it leaves the screen
        if self.rect.top == sHeight:
            self.kill()



def waitForEsc():
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

def generateMob(*args):
    # generate new mobs
    # args are groups sprite needs to join
    bubba = Mob(random.choice(enemy_list))
    for i in args:
        i.add(bubba)

def drawText(surface, text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface, text_rect)

def drawShieldBar(surface, x, y, value):
    if value < 0:
        value = 0

    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = int((value/100)*BAR_LENGTH)

    outlineRect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fillRect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fillRect)
    pygame.draw.rect(surface, WHITE, outlineRect, 2)

def drawLives(surface, x, y, lives, image):
    for i in range(lives):
        img_rect = image.get_rect()
        img_rect.x = x + (img_rect.width * i)
        img_rect.y = y
        surface.blit(image, img_rect)

def gameOverScreen():
    drawText(screen, 'Aliens Invading',\
        50, sWidth/2, sHeight/4, GOLD)
    drawText(screen, 'Arrow keys move, Space to fire',\
        15, sWidth/2, sHeight/2, WHITE)
    drawText(screen, 'Press any key to start',\
        25, sWidth/2, sHeight*(3/4), WHITE)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        waitForEsc()
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False
    
    

def mainLoop():
    '''main game loop'''
    
     # start background music
    pygame.mixer.music.play(loops=-1)
    screen.blit(bg, (0,0))
            
    game_over = True
    looping = True
    while looping:
        if game_over == True:
            gameOverScreen()
            game_over = False
            all_sprites = pygame.sprite.Group()
            mobs = pygame.sprite.Group()
            apples = pygame.sprite.Group()
            powerups = pygame.sprite.Group()
        
            # create player
            player1 = Player(player_img)
            all_sprites.add(player1)
            score = 0
        
            # create mobs
            for i in range(8):
                generateMob(mobs, all_sprites)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        # run all spirtes update functions
        all_sprites.update()

        # throw apples at aliens
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            player1.throw(apple_img, all_sprites, apples)

        # does apple touch mob
        strikes = pygame.sprite.groupcollide(\
            mobs, apples, True, True, pygame.sprite.collide_circle)
        for strike in strikes:
            score += abs((strike.radius*2)-70)# extra score for small mobs
            teleportSound.play()
            expl = Explosion(strike.rect.center, 'lg')
            all_sprites.add(expl)
            # randomly spawn powerups after alien disappear
            if random.random() > .95:
                steve = Powerup(strike.rect.center)
                all_sprites.add(steve)
                powerups.add(steve) 
            generateMob(mobs, all_sprites) # regenerate mob            
                        
        # does mob touch player
        hits = pygame.sprite.spritecollide(\
            player1,mobs, True, pygame.sprite.collide_circle)
        for hit in hits:
            generateMob(mobs, all_sprites) # regenerate mob
            player1.shield -= hit.radius*2 # lessen sheild
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
            if player1.shield <= 0:
                treeExpl = Explosion(player1.rect.center, 'player')
                all_sprites.add(treeExpl)
                player1.lives -= 1
                player1.hide()
                player1.shield = 100
                
        # does player touch powerup
        extraPowers = pygame.sprite.spritecollide(\
            player1, powerups, True)
        for i in extraPowers:
            if i.option == 'shield':
                player1.shield += random.randrange(10,31, 5)
                if player1.shield > 100:
                    player1.shield = 100
            elif i.option == 'throw':
                player1.powerThrow()
            elif i.option == 'bad':
                if player1.shield >= 50:
                    player1.shield = 5
                    # play some sound
                else:
                    treeExpl = Explosion(player1.rect.center, 'player')
                    all_sprites.add(treeExpl)
                    player1.lives -= 1
                    player1.hide()
                    player1.shield = 100
                
        # if player out of lives and sonic explosion animation finished
        if player1.lives == 0 and not treeExpl.alive():
            game_over = True


        # Draw / render
        screen.fill(GREY)
        screen.blit(bg, (0,0))
        all_sprites.draw(screen)
        
        #draw score
        drawText(screen, str(score), 30, sWidth/2, 10, WHITE)
        drawShieldBar(screen, 5,5, player1.shield)
        drawLives(screen, \
            sWidth-(img_mini.get_rect().width*player1.lives),\
            5, player1.lives, img_mini)
        
        pygame.display.flip()
        clock.tick(fps)

        waitForEsc()
    pygame.quit()
    sys.exit


if __name__ =='__main__':
    mainLoop()


