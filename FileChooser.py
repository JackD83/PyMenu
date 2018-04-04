import RenderObject, Configuration, AbstractList
import os, Keys, RenderControl, Common
import pygame, sys
from operator import itemgetter

class FileChooser(AbstractList.AbstractList):
   
    folderIcon = Common.loadImage( "theme/folder.png")
    fileIcon =  Common.loadImage( "theme/file.png")
   
    currentSelection =""
    previewTmp = None

    def renderText(self, entry):
        text = self.entryFont.render(entry["name"], True, self.textColor)
        entry["text"] = text
        return text
 
    def renderEntry(self, screen, index, yOffset):
        text = self.entryList[index]["text"]
        if(text== None):
            text = self.renderText(self.entryList[index])

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
        if(len(self.entryList) == 0):
            self.callback(None)
            return

        if(self.entryList[self.currentIndex]["isFolder"]):
            self.loadFolder(self.entryList[self.currentIndex])
        else:
            self.callback(os.path.normpath(self.currentPath + "/" + self.entryList[self.currentIndex]["name"]))
    
    def onExit(self):
        if(self.selectFolder):
            self.callback(os.path.normpath(self.initialPath))
        else:
            self.callback(None)
    
    def onChange(self):
        if(len(self.entryList) == 0):
            self.currentSelection = None
            self.previewPath = None
            return

        self.currentSelection = self.currentPath + "/" + self.entryList[self.currentIndex]["name"]
        self.currentSelection =  os.path.normpath(self.currentSelection)
        self.previewPath = None

        if("directPreview" in self.options and self.options["directPreview"] and self.isImage()):
             self.previewPath = self.currentSelection
             print("onChange" + self.previewPath)
             return
        if("previews" in self.options and self.options["previews"] != None and os.path.exists(self.options["previews"]) and self.currentSelection != None):
            self.previewPath = self.options["previews"] + "/" + os.path.splitext(os.path.basename(self.currentSelection))[0] + ".png"
        
            if(not self.previewPath != None and not os.path.exists(self.previewPath)):
                self.previewPath = None
       


    def handleEvents(self, events):     
        for event in events:    
            if event.type == pygame.KEYDOWN:         
                if event.key == Keys.DINGOO_BUTTON_START:
                    if(self.selectFolder):
                          self.callback(self.currentPath)
                          RenderControl.setDirty()
                          return
           
                    
               

        AbstractList.AbstractList.handleEvents(self, events)

   
    def initList(self):
        print(self.currentPath)
        if(os.path.isdir(self.currentPath)):
            self.entryList = []
            entry = {}
            entry["name"] = ".."
            entry["isFolder"] = True
            entry["text"] = self.entryFont.render("..", True, self.textColor)
            self.entryList.append(entry)

            try:
                for f in sorted(os.listdir(self.currentPath)):
                    if(os.path.isdir(self.currentPath + "/" + f)):
                        entry = {}
                        entry["name"] = f
                        entry["isFolder"] = True
                        entry["text"] = None
                        self.entryList.append(entry)
                for f in sorted(os.listdir(self.currentPath)):
                    if(not os.path.isdir(self.currentPath + "/" + f) and not self.selectFolder and self.filterFile(f)):
                        entry = {}
                        entry["name"] = f
                        entry["isFolder"] = False
                        entry["text"] = None
                        self.entryList.append(entry)
            except Exception as ex:
                pass            
        self.onChange()


    def getExistingParent(self, path):
        if(path == "/" or path == ""):
            return "/"

        parent = os.path.abspath(os.path.join(path, os.pardir))
        if(parent == path):
            return path

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
    
  

    def __init__(self, screen, titel, initialPath, selectFolder, options, callback):        
        AbstractList.AbstractList.__init__(self,screen, titel, options)

        if(initialPath == None):
            initialPath = "/"

        self.getExistingParent(initialPath)

        if(os.path.exists(initialPath) and not os.path.isfile(initialPath)):          
            self.currentPath = initialPath
        else:
            self.currentPath = self.getExistingParent(initialPath)

        if("directPreview" in self.options and self.options["directPreview"]):
            self.previewEnabled = True

        if("previews" in self.options and self.options["previews"] != None and os.path.exists(self.options["previews"]) ):
            self.previewEnabled = True
        
           
        self.currentSelection = initialPath
        self.initialPath = initialPath       
        self.selectFolder = selectFolder  
        self.callback = callback

        self.yFolderOffset = (self.listEntryHeight - self.folderIcon.get_height()) / 2
        self.xFolderOffset = (self.listEntryHeight - self.folderIcon.get_width()) / 2

        self.yFileOffset =  (self.listEntryHeight - self.fileIcon.get_height()) / 2
        self.xFileOffset =  (self.listEntryHeight - self.fileIcon.get_width()) / 2

        self.initList()
  
      