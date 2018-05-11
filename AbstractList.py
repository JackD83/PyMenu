import RenderObject, Configuration, Footer
import os, Keys, RenderControl, Common, TaskHandler
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

    previewCache = {}
    previewEnabled = False
    previewPath = None
    preview_final = None

    previewBoxSize = 200

    useSidebar = False
    sidebarWidth = 138

    headerHeight = 42
    initialPath =""
      
    titleFont = pygame.font.Font('theme/NotoSans-Regular.ttf', 15)
    entryFont = pygame.font.Font('theme/NotoSans-Regular.ttf', 12)
    descriptionFont = pygame.font.Font('theme/NotoSans-Regular.ttf', 12)

    maxListEntries = 13  

    currentIndex = 0
    currentWrap = 0

    def render(self, screen):
        screen.blit(self.background, (0,0))
        self.renderHeader(screen)
        self.renderSidebar(screen)
  
        self.renderEntries(screen)
        self.renderSelection(screen)

        self.renderScrollbar(screen)

        self.renderPreview(screen)

        self.footer.render(screen)
    
    def renderScrollbar(self, screen):
        shouldBe = self.listEntryHeight * (len(self.entryList) - self.maxListEntries)
        if(shouldBe <= self.listHeight):
            return

        percent = self.listHeight / shouldBe
        barHeight = self.listHeight * percent

        scrollRest = self.listHeight - barHeight
      
        progress = self.currentWrap * self.listEntryHeight
        percentProgress = progress / shouldBe

        offset = scrollRest * percentProgress

        pygame.draw.line(screen, (105,105,105), (self.config["screenWidth"] - 3, offset), (self.config["screenWidth"] - 3, offset + barHeight), 2)



        #print("is " + str(progress) + " should " + str(percentProgress))

    def renderPreview(self, screen):
        return

        if(not self.previewEnabled):
            return
        
        if(self.currentIndex == -1):
            print("index - 1")
            return

        if(not self.useSidebar):
            previewBox = pygame.Surface((self.previewBoxSize, self.previewBoxSize))
            previewBox.fill(Configuration.toColor(self.theme["side"]["color"]))

        if(self.preview_final != None and os.path.exists(self.preview_final)):
            print("render " + self.preview_final)
                 
            image = None
            if(not self.preview_final in self.previewCache):
                image = Common.loadImage(self.preview_final)

                if(not self.useSidebar):
                    image = Common.aspect_scale(image, self.previewBoxSize - 10, self.previewBoxSize - 10)
                else:
                    image = Common.aspect_scale(image, 128, 128)
                
                self.previewCache[self.preview_final] = image
            else:
                image = self.previewCache[self.preview_final]


            if(not self.useSidebar):
                xOffset = (previewBox.get_width() - image.get_width()) / 2
                yOffset = (previewBox.get_height() - image.get_height()) / 2
                previewBox.blit(image,(xOffset,yOffset))
            else:
                xOffset = (128 - image.get_width()) / 2
                yOffset = (128 - image.get_height()) / 2
                screen.blit(image,(5 + xOffset,56 + yOffset))


        if(not self.useSidebar):
            screen.blit(previewBox, (self.config["screenWidth"] - previewBox.get_width() ,self.headerHeight))
        

    def renderHeader(self, screen):
        if(not self.useSidebar):
            screen.blit(self.header, (0,0))

    def renderSidebar(self, screen):
        if(self.useSidebar):
            screen.blit(self.sidebar, (0,0))

    def renderSelection(self, screen):
        if(len(self.entryList) == 0):
            self.currentIndex = -1
            return
        

        offset = self.listEntryHeight * (self.currentIndex - self.currentWrap) + self.headerHeight
        screen.blit(self.selection, (self.sidebarWidth,offset))

    def handleEvents(self, events):
        for event in events:    
            if event.type == pygame.KEYDOWN:
                if(not len(self.entryList) <= 1):              
                    self.preview_final = None

                if event.key == Keys.DINGOO_BUTTON_UP:
                    if(not len(self.entryList) <= 1):
                        self.up()
                        self.onChange()
                        RenderControl.setDirty()
                if event.key == Keys.DINGOO_BUTTON_DOWN:
                    if(not len(self.entryList) <= 1):   
                        self.down()
                        self.onChange()
                        RenderControl.setDirty()
                if event.key == Keys.DINGOO_BUTTON_L:
                    self.up(self.maxListEntries)
                    self.onChange()
                    RenderControl.setDirty()
                if event.key == Keys.DINGOO_BUTTON_R:
                    self.down(self.maxListEntries)
                    self.onChange()
                    RenderControl.setDirty()
                if event.key == Keys.DINGOO_BUTTON_A:
                    self.onSelect()
                    RenderControl.setDirty()
                if event.key == Keys.DINGOO_BUTTON_B:
                    self.onExit()
                    RenderControl.setDirty()
                if event.key == Keys.DINGOO_BUTTON_Y:
                    self.previewEnabled = not self.previewEnabled
                    RenderControl.setDirty()
            if event.type == pygame.KEYUP:
               self.preview_final = self.previewPath
               RenderControl.setDirty()

    def onSelect(self):
        pass
    
    def onExit(self):
        pass

    def onChange(self):
        if(len(self.entryList) <= 1):
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
            self.renderEntry(screen, i + self.currentWrap, self.sidebarWidth, i * self.listEntryHeight + self.headerHeight)

        
    def up(self, count=1):
        self.currentIndex -= count
        if(self.currentIndex  < 0):
            self.currentIndex = 0
        
        if(self.currentIndex  <= self.currentWrap):
            self.currentWrap -= count
        
        if(self.currentWrap < 0 or len(self.entryList) < self.maxListEntries):
            self.currentWrap = 0
    
    def down(self, count=1):
        self.currentIndex += count
        if(self.currentIndex > len(self.entryList) - 1 ):
            self.currentIndex = len(self.entryList) - 1

        if(self.currentIndex >= self.maxListEntries + self.currentWrap):
            self.currentWrap += count

        if(self.currentWrap > len(self.entryList) - self.maxListEntries):
            self.currentWrap = len(self.entryList) - self.maxListEntries   
        
        if(len(self.entryList) < self.maxListEntries):
            self.currentWrap = 0

    def initBackground(self):       
        if("background" in self.options):
            self.background = pygame.transform.scale(Common.loadImage(self.options["background"]), (self.config["screenWidth"],self.config["screenHeight"]))
            surface =  pygame.Surface((self.config["screenWidth"],self.config["screenHeight"]), pygame.SRCALPHA)
            surface.fill(self.backgroundColor)
            self.background.blit(surface, (0,0))          
        else:
            self.background = pygame.Surface((self.config["screenWidth"],self.config["screenHeight"]))
            self.background.fill(self.backgroundColor)

        #for i in range(0, self.maxListEntries):
            #y = i * self.listEntryHeight + self.headerHeight
            #pygame.draw.line(self.background, (105,105,105), (self.sidebarWidth, y), (self.config["screenWidth"], y), 1)

    def initHeader(self):
        self.header = pygame.Surface((self.config["screenWidth"], self.headerHeight))
        self.header.fill(Configuration.toColor(self.theme["side"]["color"]))
        self.initFolderIcon(self.header)
        self.titleText = self.titleFont.render(self.title, True,(255,255,255))
        yOffset = 0
        if(self.titleText.get_height() < 20):
                yOffset = ((20 - self.titleText.get_height()) / 2)

        x = 5
        if("folderIcon" in self.options):
            x = 42

        self.header.blit(self.titleText, (x, 5 + yOffset))

        if("description" in self.options):
            description = self.descriptionFont.render(self.options["description"], True,(255,255,255))
            if(description.get_height() < 9):
                yOffset = ((9 - description.get_height()) / 2)

            self.header.blit(description, (x, 20 + yOffset))
    
    def initSidebar(self):
        self.sidebar = pygame.Surface((self.sidebarWidth, self.config["screenHeight"]))
        self.sidebar.fill(Configuration.toColor(self.theme["side"]["color"]))
        self.initFolderIcon(self.sidebar)
        self.titleText = self.titleFont.render(self.title, True,(255,255,255))
        yOffset = 0
        if(self.titleText.get_height() < 32):
                yOffset = ((32 - self.titleText.get_height()) / 2)

        x = 5
        if("folderIcon" in self.options):
            x = 42

        self.sidebar.blit(self.titleText, (x, 5 + yOffset))

        if("description" in self.options):
            description = self.entryFont.render(self.options["description"], True,(255,255,255))
            if(self.titleText.get_height() < 32):
                yOffset = ((9 - description.get_height()) / 2)

            self.sidebar.blit(description, (5, 42 + yOffset))
        

    def initFolderIcon(self, surface):
        if("folderIcon" in self.options):
            icon = Common.aspect_scale(Common.loadCachedImage(self.options["folderIcon"]), 32, 32)
            if(icon.get_width() == 32):
                xOffset = 0
            else:
                xOffset = (32 - icon.get_width()) / 2
            if(icon.get_height() == 32):
                yOffset = 0
            else:
                yOffset = (32 - icon.get_height()) / 2

            surface.blit(icon, (5 + xOffset , 5 + yOffset))
        
        
   
    def initSelection(self):
        self.selection = pygame.Surface((self.config["screenWidth"] - self.sidebarWidth,self.listEntryHeight),pygame.SRCALPHA)
        self.selection.fill((55,55,55, 120))

    def setFooter(self, footer):
        self.footer = footer
        self.listHeight = self.config["screenHeight"] - self.headerHeight
        self.listEntryHeight = int(self.listHeight / self.maxListEntries)

    def updateFooterPos(self, start, target, current, finished):
        if(not finished):
            self.footer.setYPosition(current)
        else:
            self.footer.setEnabled(False)
        
        RenderControl.setDirty()
        

    def __init__(self, screen, titel, options):
        self.screen = screen           
       
        self.title = titel
        self.options = options
        self.setFooter(Footer.Footer([],[],(255,255,255)))

        self.previewBoxSize = int(self.config["screenWidth"] * 0.5)
        if(self.previewBoxSize > 200):
            self.previewBoxSize = 200
       

        if("textColor" in self.options):
            self.textColor = options["textColor"]
        else:
            self.textColor = (0,0,0)
        
        if("backgroundColor" in self.options):
            self.backgroundColor = options["backgroundColor"]
        else:
            self.backgroundColor = (221,221,221, 160)
               
      
        if("useSidebar" in options and options["useSidebar"]):
            self.useSidebar = True
            self.headerHeight = 0
            self.initSidebar()
        else:
            self.useSidebar = False
            self.sidebarWidth = 0
            self.initHeader()
        
        self.listHeight = self.config["screenHeight"] - self.headerHeight
        self.listEntryHeight = int(self.listHeight / self.maxListEntries)
        self.initBackground()

        self.initSelection()

        TaskHandler.addAnimation(self.config["screenHeight"] - self.footer.getHeight(), self.config["screenHeight"], 600, self.updateFooterPos, 1000) 

       