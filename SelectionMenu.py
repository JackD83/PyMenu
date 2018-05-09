import RenderObject, Configuration
import os, Keys, RenderControl
import pygame, sys

class SelectionMenu(RenderObject.RenderObject):

    optionHeight = 30
    width = 150
    height = 0
    maxOptionHeight = optionHeight * 5
    menuAlpha = 230
    maxRenderItems = 0

    config = Configuration.getConfiguration()

    background = None
    options = None
    currentIndex = 0
    wrapIndex = 0
    optionsText = []
    selection = None

    

    def init(self):
        self.height = len(self.options) * self.optionHeight
        if(self.height > self.maxOptionHeight):
            self.wrap = True
            self.height = self.maxOptionHeight
            print("wrapping")

        self.x = (self.config["screenWidth"] - self.width) / 2
        self.y = (self.config["screenHeight"] - self.height) / 2

    def renderBackground(self):
        self.background = pygame.Surface((self.width,self.height),pygame.SRCALPHA)
        self.background.fill((220,220,220, self.menuAlpha))
        self.maxRenderItems = int(self.height / self.optionHeight)

        for x in range(1, int(self.height / self.optionHeight)):
            pygame.draw.line(self.background, (105,105,105, self.menuAlpha- 30), (0, x * self.optionHeight), (self.width, x * self.optionHeight), 1)


    def initOptionText(self):
        self.optionsText = []
        font = pygame.font.Font('theme/NotoSans-Regular.ttf', 20)
        for opt in self.options: 
            text = font.render(opt, True, (105,105,105))
            self.optionsText.append(text)

    def renderOptionText(self):
        for i in range(0, self.maxRenderItems):          
            text = self.optionsText[i + self.wrapIndex]
            yOffset = (self.optionHeight -  text.get_height()) / 2

            self.background.blit(text, (10, i * self.optionHeight + yOffset))
           


           # text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            #screen.blit(text, text_rect)
    def renderSelection(self):
        offset = self.optionHeight * (self.currentIndex - self.wrapIndex)
        self.background.blit(self.selection, (0,offset))

    def render(self, screen):
        self.renderBackground()
        self.renderOptionText()
        self.renderSelection()
        screen.blit(self.background, (self.x,self.y))


    def handleEvents(self, events):    
        for event in events:    
            if event.type == pygame.KEYDOWN:           
                if event.key == Keys.DINGOO_BUTTON_UP:
                    self.up()
                    RenderControl.setDirty()
                if event.key == Keys.DINGOO_BUTTON_DOWN:
                    self.down()
                    RenderControl.setDirty()
                if event.key == Keys.DINGOO_BUTTON_A:
                    self.callback(self.currentIndex, self.options[self.currentIndex])
                    RenderControl.setDirty()
                if event.key == Keys.DINGOO_BUTTON_B:
                    self.callback(-1, None)
                    RenderControl.setDirty()

    def down(self):
        self.currentIndex += 1
        if(self.currentIndex > len(self.options) - 1 ):
            self.currentIndex = len(self.options) -1

        if(self.currentIndex > self.maxRenderItems + self.wrapIndex + -1):
            self.wrapIndex += 1
           
        
    
    def up(self):
        self.currentIndex -= 1
        if(self.currentIndex  < 0):
            self.currentIndex = 0
        
        if(self.currentIndex  < self.wrapIndex):
            self.wrapIndex -= 1
           
        

    
    def __init__(self, screen, options, callback):
        print("Opened Options menu ", options)
        self.options = options
        self.callback = callback
        self.selection = pygame.Surface((self.width,self.optionHeight),pygame.SRCALPHA)
        self.selection.fill((255,255,255, 180))

        self.init()
        self.initOptionText()
