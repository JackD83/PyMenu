import RenderObject, Configuration
import os, Keys, RenderControl
import pygame, sys
import Theme

class SelectionMenu(RenderObject.RenderObject):

    optionHeight = 18
    width = 150
    height = 0
    maxOptionHeight = optionHeight * 5
    menuAlpha = 255
    maxRenderItems = 0

    config = Configuration.getConfiguration()

    background = None
    backgroundShadow = None
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

        self.backgroundShadow = pygame.Surface((self.width,self.height),pygame.SRCALPHA)
        self.backgroundShadow.fill((0,0,0, 120))

    def renderBackground(self):
        self.background = pygame.Surface((self.width,self.height))
        self.background.fill(Theme.getColor("selectionMenu/backgroundColor", (255,255,255)))


        self.maxRenderItems = int(self.height / self.optionHeight)

        for x in range(1, int(self.height / self.optionHeight)):
            pass
            #pygame.draw.line(self.background, (105,105,105, self.menuAlpha), (0, x * self.optionHeight), (self.width, x * self.optionHeight), 1)


    def initOptionText(self):
        self.optionsText = []
        font = pygame.font.Font('theme/NotoSans-Regular.ttf', 14)
        for opt in self.options: 
            text = font.render(opt, True,Theme.getColor("selectionMenu/fontColor", (55,55,55)))
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

        screen.blit(self.backgroundShadow, (self.x + 4,self.y + 4))
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
           
        

    
    def __init__(self, screen, options, callback, width=150):
        print("Opened Options menu ", options)
        self.options = options
        self.callback = callback
        self.width = width

        self.selection = pygame.Surface((self.width,self.optionHeight),pygame.SRCALPHA)
        self.selection.fill(Theme.getColor("selectionMenu/selectionColor", (55,55,55,120)))

     

        self.init()
        self.initOptionText()
