import pygame as pg
from pygame.locals import *
import Colours as c
import random

clock = pg.time.Clock()
pg.time.set_timer(USEREVENT + 1, 500)
pg.time.set_timer(USEREVENT + 2, random.randrange(3500, 4500))


class Setup:

    def __init__(self):
        pg.init()

        self.hitboxon = False
        self.screenHeight = 600
        self.screenWidth = 1000
        self.screen1x = 0

        self.speed = 30

        self.background = pg.image.load('background.png')
        self.background = pg.transform.scale(self.background, (1568, 600))

        self.screen2x = self.background.get_width()

        self.screen = pg.display.set_mode((self.screenWidth, self.screenHeight))

    def mainloop(self):
        self.obstacles = []
        self.running = True
        while self.running:
            clock.tick(self.speed)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    continue
                if event.type == USEREVENT + 1:
                    self.speed += 1

                if event.type == USEREVENT + 2:
                    r = random.randrange(1, 3)

                    if r == 1:
                        self.obstacles.append(Barrior(1000, 0, 128, 380, r))
                    elif r == 2:
                        r2 = random.randrange(0,2)
                        self.obstacles.append(Barrior(1000, 420 - (r2*100) , 20, 64 + (r2*100), r))
                if event.type == KEYDOWN:
                    if player.isjump and not player.isdoublejump and event.key == K_w:
                        player.isdoublejump = True
                        player.doublejumpcount = 10
                    if not player.isjump and not player.iscrouch and not player.isdoublejump:
                        if event.key == K_w:
                            player.isjump = True
                            player.jumpcount = 10
                        if event.key == K_s:
                            player.iscrouch = True
                            player.crouchcount = 76
                    if event.key == K_h:
                        if self.hitboxon:
                            self.hitboxon = False
                        else:
                            self.hitboxon = True

            self.screen1x -= 3
            self.screen2x -= 3

            if self.screen1x < self.background.get_width() * -1:
                self.screen1x = self.background.get_width()
            if self.screen2x < self.background.get_width() * -1:
                self.screen2x = self.background.get_width()

            player.frame()
            # self.screen.fill(c.BLACK)
            self.redrawscreen()

            pg.display.update()

            if not player.alive:
                root.screen.fill(c.BLACK)
                self.speed=10
                #root.screen.blit(self.background, (self.screen1x, 0))
                #root.screen.blit(self.background, (self.screen2x, 0))
                player.deathan()
                pg.display.update()


        pg.quit()

    def redrawscreen(self):
        root.screen.blit(self.background, (self.screen1x, 0))
        root.screen.blit(self.background, (self.screen2x, 0))
        player.draw()
        for obstical in self.obstacles:
            obstical.draw()
            if obstical.collide(player.hitbox):
                player.alive = False
        try:
            if self.obstacles[0].x + self.obstacles[0].width <= 0:
                self.obstacles.pop(0)
        except:
            pass


class Player:
    def __init__(self):
        self.alive = True
        self.x = 150
        self.y = 350
        self.width = 50
        self.height = 150
        self.idlepos = pg.image.load('idle.png')

        self.deathpos = [pg.image.load('death-1.png'), pg.image.load('death-2.png'), pg.image.load('death-3.png'),
                         pg.image.load('death-4.png'), pg.image.load('death-5.png')]
        for i in range(5):
            self.deathpos[i] = pg.transform.scale(self.deathpos[i], (150, 150))
        self.deathcount = 0
        self.hitbox = (self.x + 22, self.y, self.width, self.height)

        self.isjump = False
        self.jumpcount = 10
        self.jumppos = [pg.image.load('jump-1.png'), pg.image.load('jump-2.png'), pg.image.load('jump-3.png'),
                        pg.image.load('jump-4.png'), pg.image.load('jump-5.png'), pg.image.load('jump-6.png'),
                        pg.image.load('jump-7.png'), pg.image.load('jump-8.png')]
        for i in range(8):
            self.jumppos[i] = pg.transform.scale(self.jumppos[i], (150, 195))
        self.isdoublejump = False
        self.doublejumpcount = 10

        self.isdoublejumpdrop = False

        self.doublejumpdropcount = 0

        self.iscrouch = False
        self.crouchcount = 45
        self.crouchheight = self.height * 0.75
        self.crouchy = self.y + self.crouchheight
        self.crouchpos = [pg.image.load('roll-1.png'), pg.image.load('roll-2.png'), pg.image.load('roll-3.png'),
                          pg.image.load('roll-4.png'), pg.image.load('roll-5.png'), pg.image.load('roll-6.png'),
                          pg.image.load('roll-3.png'),
                          pg.image.load('roll-4.png'), pg.image.load('roll-5.png'), pg.image.load('roll-6.png'),
                          pg.image.load('roll-3.png'),
                          pg.image.load('roll-4.png'), pg.image.load('roll-5.png'), pg.image.load('roll-6.png'),
                          pg.image.load('roll-3.png'),
                          pg.image.load('roll-4.png'), pg.image.load('roll-5.png'), pg.image.load('roll-6.png'),
                          pg.image.load('roll-7.png')]
        for i in range(19):
            self.crouchpos[i] = pg.transform.scale(self.crouchpos[i], (150, 150))
        self.walkpos = [pg.image.load('walk-4.png'), pg.image.load('walk-3.png'), pg.image.load('walk-2.png'),
                        pg.image.load('walk-1.png')]
        for i in range(4):
            self.walkpos[i] = pg.transform.scale(self.walkpos[i], (150, 150))

        self.walkcount = 0

    def walk(self):
        self.walkcount += 1
        if self.walkcount == 12:
            self.walkcount = 0

        root.screen.blit(self.walkpos[self.walkcount // 3], (self.x, self.y))


    def draw(self):

        if self.iscrouch:
            self.hitbox = (self.x + 48, self.y + 40, self.width, self.height)
        else:
            self.hitbox = (self.x + 48, self.y, self.width, self.height)
        if root.hitboxon:
            pg.draw.rect(root.screen, c.RED, self.hitbox, 2)
        if self.iscrouch:
            root.screen.blit(self.crouchpos[(76 - self.crouchcount) // 4], (self.x, self.y))
        elif self.isjump:
            if self.jumpcount >= 9:
                index = 0
            elif self.jumpcount >= 7:
                index = 1
            elif self.jumpcount >= 3:
                index = 2
            elif self.jumpcount >= 1:
                index = 3
            elif self.jumpcount >= -1:
                index = 4
            elif self.jumpcount >= -5:
                index = 5
            else:
                index = 6
            root.screen.blit(self.jumppos[index], (self.x, self.y))
        elif self.isdoublejump:
            if self.doublejumpcount >= 9:
                index = 0
            elif self.doublejumpcount >= 7:
                index = 1
            elif self.doublejumpcount >= 3:
                index = 2
            elif self.doublejumpcount >= 0:
                index = 3
            elif self.doublejumpdropcount >= -5:
                index = 4
            elif self.doublejumpdropcount >= -7:
                index = 5
            else:
                index = 6
            root.screen.blit(self.jumppos[index], (self.x, self.y))
        else:
            self.walk()
    def deathan(self):


        root.screen.blit(self.deathpos[self.deathcount // 5], (self.x, self.y))
        self.deathcount += 1
        if self.deathcount == 25:
            root.running = False

    def frame(self):
        self.doubleJump()
        self.jump()

        self.crouch()

    def jump(self):

        if self.isjump:

            if self.jumpcount >= -10:
                self.y -= (self.jumpcount * abs(self.jumpcount)) * 0.15
                self.jumpcount -= 0.3
            else:
                self.isjump = False
                self.y = self.crouchy - self.crouchheight
    def doubleJump(self):
        if self.isdoublejumpdrop:
            self.doubleJumpDrop(False)
        else:
            if self.isdoublejump:
                self.isjump = False
                if self.doublejumpcount >= 0:
                    self.y -= (self.doublejumpcount * abs(self.doublejumpcount)) * 0.15
                    self.doublejumpcount -= 0.3
                else:

                    self.doubleJumpDrop(True)

    def doubleJumpDrop(self, start):

        if start:
            self.doublejumpdropcount = 0

            self.isdoublejumpdrop = True

        if self.isdoublejumpdrop:

            if self.doublejumpdropcount >= -20:
                self.y -= (self.doublejumpdropcount * abs(self.doublejumpdropcount)) * 0.15
                self.doublejumpdropcount -= 0.3
            else:
                self.isdoublejumpdrop = False
                self.isdoublejump = False

            if self.y >= (self.crouchy - self.crouchheight):
                self.y = self.crouchy - self.crouchheight
                self.isdoublejumpdrop = False
                self.isdoublejump = False

    def crouch(self):

        if self.iscrouch:
            self.height = self.crouchheight

            self.crouchcount -= 1

            if self.crouchcount == 0:
                self.height = 150

                self.iscrouch = False


class Barrior:

    def __init__(self, x, y, width, height, type):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 3
        self.type = type
        if self.type == 1:
            self.image = pg.image.load('barrior.png')
            self.image = pg.transform.scale(self.image, (self.width, self.height))
        elif self.type == 2:
            self.image = pg.image.load('spike.png')
            self.image = pg.transform.scale(self.image, (self.width, self.height))
        self.draw()

    def draw(self):
        self.hitbox = (self.x,self.y,self.width,self.height)

        root.screen.blit(self.image, (self.x, self.y))
        if root.hitboxon:
            pg.draw.rect(root.screen, c.RED, self.hitbox, 2)
        self.x -= self.vel

    def collide(self, rect):

        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:

            if rect[1] + rect[3] > self.hitbox[1] and self.type == 2:
                return True
            if (rect[1] < self.hitbox[3]) and self.type == 1:
                return True
        return False


root = Setup()

player = Player()
root.mainloop()
