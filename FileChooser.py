import RenderObject, Configuration
import os
import pygame, sys
from operator import itemgetter

class FileChooser(RenderObject.RenderObject):
    config = Configuration.getConfiguration()
    theme = Configuration.getTheme()
    pygame.font.init()
    entryList = []
    background = None
    selection = None
    footerHeight = 24
    headerHeight = 20
    initialPath =""
    
    titleFont = pygame.font.Font('theme/FreeSans.ttf', 20)
    entryFont = pygame.font.Font('theme/FreeSans.ttf', 16)
    folderIcon = pygame.image.load( "theme/folder.png")
    fileIcon =  pygame.image.load( "theme/file.png")

    listHeight = config["screenHeight"] - headerHeight - footerHeight
    maxListEntries = 11
    listEntryHeight = int(listHeight / maxListEntries)

    currentIndex = 0
    currentWrap = 0

    def render(self, screen):
        screen.blit(self.background, (0,0))
        self.renderHeader(screen)
        self.renderFooter(screen)
        self.renderEntries(screen)
        self.renderSelection(screen)
        self.renderPreview(screen)

    def renderHeader(self, screen):
        screen.blit(self.header, (0,0))

    def renderFooter(self, screen):
        screen.blit(self.footer, (0,self.config["screenHeight"] - self.footerHeight))
    
    def renderPreview(self, screen):
        previewBox = pygame.Surface((200, 200), pygame.SRCALPHA)
        previewBox.fill(Configuration.toColor(self.theme["footer"]["color"]))
        screen.blit(previewBox, (self.config["screenWidth"] - previewBox.get_width() ,self.headerHeight))

    def renderEntries(self, screen):

        max = 0
        if(len(self.entryList) >  self.maxListEntries ):
            max = self.maxListEntries
        else:
            max = len(self.entryList)

        yFolderOffset = (self.listEntryHeight - self.folderIcon.get_height()) / 2
        xFolderOffset = (self.listEntryHeight - self.folderIcon.get_width()) / 2

        yFileOffset =  (self.listEntryHeight - self.fileIcon.get_height()) / 2
        xFileOffset =  (self.listEntryHeight - self.fileIcon.get_width()) / 2

        for i in range(0, max):
            text = self.entryList[i + self.currentWrap]["text"]
            yOffset = (self.listEntryHeight -  text.get_height()) / 2

            screen.blit(text, (self.listEntryHeight + 4, i * self.listEntryHeight + yOffset + self.headerHeight + 1))
            if(self.entryList[i + self.currentWrap]["isFolder"]):
                screen.blit(self.folderIcon, (xFolderOffset, i * self.listEntryHeight + self.headerHeight + yFolderOffset) )
            else:
                screen.blit(self.fileIcon, (xFileOffset, i * self.listEntryHeight + self.headerHeight + yFileOffset) )

    def renderSelection(self, screen):
        offset = self.listEntryHeight * (self.currentIndex - self.currentWrap) + self.headerHeight
        screen.blit(self.selection, (0,offset))

    def handleEvents(self, events):
        for event in events:    
            if event.type == pygame.KEYDOWN:         
                if event.key == pygame.K_UP:
                    self.up()
                if event.key == pygame.K_DOWN:
                    self.down()
                if event.key == pygame.K_RETURN:
                    if(self.entryList[self.currentIndex]["isFolder"]):
                        self.loadFolder(self.entryList[self.currentIndex])
                    else:
                        self.callback(self.currentPath + "/" + self.entryList[self.currentIndex]["name"])
                if event.key == pygame.K_ESCAPE:
                    self.callback(None)
            if event.type == pygame.KEYUP:
                print("key up!")

    def loadFolder(self, folder):
        if(folder["name"] == ".."):
            self.currentPath = os.path.abspath(os.path.join(self.currentPath, os.pardir))
        else:
            self.currentPath += "/" + folder["name"]
        
        print("new current path is", self.currentPath)
        self.currentWrap = 0
        self.currentIndex = 0
        self.initList()

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

    def initList(self):
        print(self.currentPath)
        if(os.path.isdir(self.currentPath)):
            self.entryList = []
            entry = {}
            entry["name"] = ".."
            entry["isFolder"] = True
            entry["text"] = self.entryFont.render("..", True, (0,0,0))
            self.entryList.append(entry)

            for f in sorted(os.listdir(self.currentPath)):
                if(os.path.isdir(self.currentPath + "/" + f)):
                    entry = {}
                    entry["name"] = f
                    entry["isFolder"] = True
                    entry["text"] = self.entryFont.render(f, True, (0,0,0))
                    self.entryList.append(entry)
            for f in sorted(os.listdir(self.currentPath)):
                if(not os.path.isdir(self.currentPath + "/" + f) and not self.selectFolder):
                    entry = {}
                    entry["name"] = f
                    entry["isFolder"] = False
                    entry["text"] = self.entryFont.render(f, True, (0,0,0))
                    self.entryList.append(entry)

    def initBackground(self):
       
        if("background" in self.options):
            self.background = pygame.image.load(self.options["background"])
            surface =  pygame.Surface((self.config["screenWidth"],self.config["screenHeight"]), pygame.SRCALPHA)
            surface.fill((255,255,255, 160))
            self.background.blit(surface, (0,0))          
        else:
            self.background = pygame.Surface((self.config["screenWidth"],self.config["screenHeight"]))
            self.background.fill((255,255,255))

        for i in range(0, self.maxListEntries):
            y = i * self.listEntryHeight + self.headerHeight
            pygame.draw.line(self.background, (105,105,105), (0, y), (self.config["screenWidth"], y), 1)

    def initHeader(self):
        self.header = pygame.Surface((self.config["screenWidth"], self.headerHeight), pygame.SRCALPHA)
        self.header.fill(Configuration.toColor(self.theme["header"]["color"]))
        self.titleText = self.titleFont.render(self.title, True, (0,0,0))
        self.header.blit(self.titleText, (4, (self.headerHeight - self.titleText.get_height()) / 2))

    def initFooter(self):
        self.footer = pygame.Surface((self.config["screenWidth"], self.footerHeight), pygame.SRCALPHA)
        self.footer.fill(Configuration.toColor(self.theme["footer"]["color"]))

    def initSelection(self):
        self.selection = pygame.Surface((self.config["screenWidth"],self.listEntryHeight),pygame.SRCALPHA)
        self.selection.fill((255,255,255, 160))

    def __init__(self, screen, titel, initialPath, selectFolder, options, callback):
        self.screen = screen
        self.currentPath = initialPath
        self.selectFolder = selectFolder
        self.callback = callback
        self.initialPath = initialPath
        self.title = titel
        self.options = options
        

        self.initList()
        self.initBackground()
        self.initHeader()
        self.initFooter()
        self.initSelection()