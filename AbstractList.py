import RenderObject, Configuration, Footer
import os, Keys, RenderControl, Common
import pygame, sys
from operator import itemgetter

class AbstractList(RenderObject.RenderObject):
    config = Configuration.getConfiguration()
    theme = Configuration.getTheme()
    pygame.font.init()
    entryList = []
    background = None
    selection = None
    footer = None

    headerHeight = 20
    initialPath =""
      
    titleFont = pygame.font.Font('theme/FreeSans.ttf', 20)
    entryFont = pygame.font.Font('theme/FreeSans.ttf', 16)
     
    maxListEntries = 12
  

    currentIndex = 0
    currentWrap = 0

    def render(self, screen):
        screen.blit(self.background, (0,0))
        self.renderHeader(screen)
    
        self.footer.render(screen)
  
        self.renderEntries(screen)
        self.renderSelection(screen)
        

    def renderHeader(self, screen):
        screen.blit(self.header, (0,0))
        

    def renderSelection(self, screen):
        if(len(self.entryList) == 0):
            return

        offset = self.listEntryHeight * (self.currentIndex - self.currentWrap) + self.headerHeight
        screen.blit(self.selection, (0,offset))

    def handleEvents(self, events):
        for event in events:    
            if event.type == pygame.KEYDOWN:         
                if event.key == Keys.DINGOO_BUTTON_UP:
                    self.up()
                    self.onChange()
                    RenderControl.setDirty()
                if event.key == Keys.DINGOO_BUTTON_DOWN:
                    self.down()
                    self.onChange()
                    RenderControl.setDirty()
                if event.key == Keys.DINGOO_BUTTON_A:
                    self.onSelect()
                    RenderControl.setDirty()
                if event.key == Keys.DINGOO_BUTTON_B:
                    self.onExit()
                    RenderControl.setDirty()
            if event.type == pygame.KEYUP:
                pass
                #print("key up!")

    def onSelect(self):
        pass
    
    def onExit(self):
        pass

    def onChange(self):
        if(len(self.entryList) == 0):
            return

        pass

    def renderEntry(self, index, yOffset):
        pass
   

    def renderEntries(self, screen):
        max = 0
        if(len(self.entryList) >  self.maxListEntries ):
            max = self.maxListEntries
        else:
            max = len(self.entryList)

        for i in range(0, max):
            self.renderEntry(screen, i + self.currentWrap, i * self.listEntryHeight + self.headerHeight)

        
    def up(self):
        self.currentIndex -= 1
        if(self.currentIndex  < 0):
            self.currentIndex = 0
        
        if(self.currentIndex  < self.currentWrap):
            self.currentWrap -= 1
    
    def down(self):
        self.currentIndex += 1
        if(self.currentIndex > len(self.entryList) - 1 ):
            self.currentIndex = len(self.entryList) -1

        if(self.currentIndex > self.maxListEntries + self.currentWrap + -1):
            self.currentWrap += 1
   

    def initBackground(self):       
        if("background" in self.options):
            self.background = Common.loadImage(self.options["background"])
            surface =  pygame.Surface((self.config["screenWidth"],self.config["screenHeight"]), pygame.SRCALPHA)
            surface.fill(self.backgroundColor)
            self.background.blit(surface, (0,0))          
        else:
            self.background = pygame.Surface((self.config["screenWidth"],self.config["screenHeight"]))
            self.background.fill(self.backgroundColor)

        for i in range(0, self.maxListEntries):
            y = i * self.listEntryHeight + self.headerHeight
            pygame.draw.line(self.background, (105,105,105), (0, y), (self.config["screenWidth"], y), 1)

    def initHeader(self):
        self.header = pygame.Surface((self.config["screenWidth"], self.headerHeight), pygame.SRCALPHA)
        self.header.fill(Configuration.toColor(self.theme["header"]["color"]))
        self.titleText = self.titleFont.render(self.title, True,self.textColor)
        self.header.blit(self.titleText, (4, (self.headerHeight - self.titleText.get_height()) / 2))
   
    def initSelection(self):
        self.selection = pygame.Surface((self.config["screenWidth"],self.listEntryHeight),pygame.SRCALPHA)
        self.selection.fill((255,255,255, 160))

    def setFooter(self, footer):
        self.footer = footer
        self.listHeight = self.config["screenHeight"] - self.headerHeight - self.footer.getHeight()
        self.listEntryHeight = int(self.listHeight / self.maxListEntries)

    def __init__(self, screen, titel, options):
        self.screen = screen           
       
        self.title = titel
        self.options = options
        self.setFooter(Footer.Footer([],[],(255,255,255)))

       

        if("textColor" in self.options):
            self.textColor = options["textColor"]
        else:
            self.textColor = (0,0,0)
        
        if("backgroundColor" in self.options):
            self.backgroundColor = options["backgroundColor"]
        else:
            self.backgroundColor = (255,255,255, 160)
               
        self.initBackground()
        self.initHeader()   
        self.initSelection()