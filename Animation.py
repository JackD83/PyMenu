import pygame, time, Common
from pygame.locals import *



class Animation(object):
    def __init__(self, filename, size):
        self.filename = filename
        self.image = None
        try:
            self.image = pygame.image.load(filename)
        except Exception as err:
            print(str(err))
        

        self.lastRenderTime = 0

        self.sizeX = size[0]
        self.sizeY = size[1]
        self.fps = Common.getFPS()
        self.valid = False

        self.cur = 0

        ix,iy = self.image.get_size()

        self.tilesX = ix / self.sizeX
        self.tilesY = iy / self.sizeY

        if(self.tilesX != 0 and self.tilesY != 0 and self.image != None):
            self.valid = True
      

    def render(self, screen, pos):
        if(not self.valid):
            return
        
        column = self.cur % self.tilesX
        row = int(self.cur / self.tilesX)

        sub = self.image.subsurface((column * self.sizeX ,row*self.sizeY, self.sizeX,self.sizeY))

        screen.blit(sub, pos) 

        self.update()

    def update(self):

        curTime = int(round(time.time() * 1000))


        if(curTime - self.lastRenderTime > 1000 / self.fps):
            self.lastRenderTime = int(round(time.time() * 1000))

            self.cur = self.cur + 1



        if(self.cur == self.tilesX * self.tilesY ):
            self.cur = 0
    
