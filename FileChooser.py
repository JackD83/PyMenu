import RenderObject, Configuration, AbstractList
import os
import pygame, sys
from operator import itemgetter

class FileChooser(AbstractList.AbstractList):
   
    folderIcon = pygame.image.load( "theme/folder.png")
    fileIcon =  pygame.image.load( "theme/file.png")

    previewCache = {}

    previewEnabled = False
    currentSelection =""

    def render(self, screen):
        super().render(screen)
        if("preview" in self.options and self.options["preview"]):
            self.renderPreview(screen)
    
    def renderPreview(self, screen):
         if("directPreview" in self.options and self.options["directPreview"] and self.isImage() and self.previewEnabled):          
            previewBox = pygame.Surface((200, 200), pygame.SRCALPHA)
            previewBox.fill(Configuration.toColor(self.theme["footer"]["color"]))

            image = None
            if(not self.currentSelection in self.previewCache):
                image = pygame.image.load(self.currentSelection)
                image = self.aspect_scale(image, 180, 180)
                self.previewCache[self.currentSelection] = image
            else:
                image = self.previewCache[self.currentSelection]

            previewBox.blit(image,(10,10))
            screen.blit(previewBox, (self.config["screenWidth"] - previewBox.get_width() ,self.headerHeight))
       
 
    def renderEntry(self, screen, index, yOffset):
        text = self.entryList[index]["text"]
        yTextOffset = (self.listEntryHeight -  text.get_height()) / 2

        screen.blit(text, (self.listEntryHeight + 4, yOffset + yTextOffset + 1))
        if(self.entryList[index]["isFolder"]):
            screen.blit(self.folderIcon, (self.xFolderOffset, yOffset +  self.yFolderOffset) )
        else:
            screen.blit(self.fileIcon, (self.xFileOffset, yOffset + self.yFileOffset) )


    def loadFolder(self, folder):
        if(folder["name"] == ".."):
            self.currentPath = os.path.abspath(os.path.join(self.currentPath, os.pardir))
        else:
            self.currentPath += "/" + folder["name"]
        
        print("new current path is", self.currentPath)
        self.currentWrap = 0
        self.currentIndex = 0
        self.initList()

    def onSelect(self):
        if(self.entryList[self.currentIndex]["isFolder"]):
            self.loadFolder(self.entryList[self.currentIndex])
        else:
            self.callback(os.path.normpath(self.currentPath + "/" + self.entryList[self.currentIndex]["name"]))
    
    def onExit(self):
        self.callback(os.path.normpath(self.initialPath))
    
    def onChange(self):
        self.currentSelection = self.currentPath + "/" + self.entryList[self.currentIndex]["name"]
        self.currentSelection =  os.path.normpath(self.currentSelection)

    def handleEvents(self, events):     
        for event in events:    
            if event.type == pygame.KEYDOWN:         
                if event.key == pygame.K_RCTRL:
                    if(self.selectFolder):
                          self.callback(self.currentPath)
                          return
                if event.key == pygame.K_TAB:
                    self.previewEnabled = not self.previewEnabled

        super().handleEvents(events)

   
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
                if(not os.path.isdir(self.currentPath + "/" + f) and not self.selectFolder and self.filterFile(f)):
                    entry = {}
                    entry["name"] = f
                    entry["isFolder"] = False
                    entry["text"] = self.entryFont.render(f, True, (0,0,0))
                    self.entryList.append(entry)


    def getExistingParent(self, path):
        parent = os.path.abspath(os.path.join(path, os.pardir))
        if(os.path.exists(parent)):
            return parent
        else:
            return self.getExistingParent(parent)

    def isImage(self):
        if(self.currentSelection.lower().endswith("png") or 
            self.currentSelection.lower().endswith("jpg") ):
            return True

    def filterFile(self, file):
        if(not "fileFilter" in self.options):
            return True #allow all files

        filename, file_extension = os.path.splitext(file)
        if(file_extension == ""):
            return False

        if any(file_extension in s for s in self.options["fileFilter"]):
            return True

        return False
    
    def aspect_scale(self, img, bx,by ):      
        ix,iy = img.get_size()
        if ix > iy:
            # fit to width
            scale_factor = bx/float(ix)
            sy = scale_factor * iy
            if sy > by:
                scale_factor = by/float(iy)
                sx = scale_factor * ix
                sy = by
            else:
                sx = bx
        else:
            # fit to height
            scale_factor = by/float(iy)
            sx = scale_factor * ix
            if sx > bx:
                scale_factor = bx/float(ix)
                sx = bx
                sy = scale_factor * iy
            else:
                sy = by

        return pygame.transform.scale(img, (int(sx),int(sy)) )

    def __init__(self, screen, titel, initialPath, selectFolder, options, callback):        
        super().__init__(screen, titel, options)

        self.getExistingParent(initialPath)

        if(os.path.exists(initialPath) and not os.path.isfile(initialPath)):          
            self.currentPath = initialPath
        else:
            self.currentPath = self.getExistingParent(initialPath)       
        
           
        self.currentSelection = initialPath
        self.initialPath = initialPath       
        self.selectFolder = selectFolder  
        self.callback = callback

        self.yFolderOffset = (self.listEntryHeight - self.folderIcon.get_height()) / 2
        self.xFolderOffset = (self.listEntryHeight - self.folderIcon.get_width()) / 2

        self.yFileOffset =  (self.listEntryHeight - self.fileIcon.get_height()) / 2
        self.xFileOffset =  (self.listEntryHeight - self.fileIcon.get_width()) / 2

        self.initList()
      