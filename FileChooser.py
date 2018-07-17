# -*- coding: utf-8 -*-
import RenderObject, Configuration, AbstractList
import os, Keys, RenderControl, Common
import pygame, sys, ResumeHandler, ntpath
from threading import Thread
from operator import itemgetter
from time import sleep

class FileChooser(AbstractList.AbstractList):
   
    folderIcon = Common.loadImage( "theme/folder.png")
    reset = None
    

   
    currentSelection = ""
    previewTmp = None

    def renderText(self, entry):
        text = self.entryFont.render(self.filterName(entry["name"]), True, self.textColor)
        entry["text"] = text
        return text
 
    def renderEntry(self, screen, index, xOffset, yOffset):
        text = self.entryList[index]["text"]
        if(text== None):
            text = self.renderText(self.entryList[index])

        yTextOffset = (self.listEntryHeight -  text.get_height()) / 2
              
        if(self.entryList[index]["isFolder"]):
            screen.blit(text, (self.listEntryHeight + 4 + xOffset, yOffset + yTextOffset))
            screen.blit(self.folderIcon, (self.xFolderOffset+ xOffset, yOffset +  self.yFolderOffset) )
        else:
            screen.blit(text, (2 + xOffset, yOffset + yTextOffset))
    

    def loadFolder(self, folder):
       
        if(folder["name"] == ".."):
           self.moveFolderUp()          
        else:
            self.currentPath += "/" + folder["name"]
            self.currentWrap = 0
            self.currentIndex = 0
            self.initList()
        
        print("new current path is", self.currentPath)
           
    def moveFolderUp(self):
        self.reset = None
        self.reset = os.path.basename(self.currentPath)
        self.currentPath = os.path.abspath(os.path.join(self.currentPath, os.pardir))
        self.currentWrap = 0
        self.currentIndex = 0
        self.initList()

        
    
    def setFooter(self, footer):
        AbstractList.AbstractList.setFooter(self, footer)
        
        
    def onSelect(self):
        if(len(self.entryList) == 0):
            self.callback(None)
            return

        if(self.entryList[self.currentIndex]["isFolder"]):
            self.loadFolder(self.entryList[self.currentIndex])
        else:
            ResumeHandler.setLastSelectedLine(self.currentIndex)
            ResumeHandler.setLastPath(os.path.normpath(self.currentPath + "/"))
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
             return
        if("previews" in self.options and self.options["previews"] != None and os.path.exists(self.options["previews"]) and self.currentSelection != None):
            self.previewPath = self.options["previews"] + "/" + os.path.splitext(os.path.basename(self.currentSelection))[0] + ".png"
        
            if(not self.previewPath != None and not os.path.exists(self.previewPath)):
                self.previewPath = None
       


    def handleEvents(self, events):     
        for event in events:    
            if event.type == pygame.KEYDOWN:                        
                if event.key == Keys.DINGOO_BUTTON_LEFT:
                    self.moveFolderUp()
                    RenderControl.setDirty()
            if event.type == pygame.KEYUP:         
                if event.key == Keys.DINGOO_BUTTON_START:
                    if(self.selectFolder):
                          self.callback(self.currentPath)
                          RenderControl.setDirty()
                    
               

        AbstractList.AbstractList.handleEvents(self, events)
   
    def initList(self):
        self.listReady = False  
        thread = Thread(target = self.initListAsync, args = ())
        thread.start()
        sleep(0.05) #allows to skip the drawing of waiting symbol if folder is loaded in 5ms
       

    def initListAsync(self):
        if(os.path.isdir(self.currentPath) and os.path.exists(self.currentPath)):
            self.entryList = []
            entry = {}
            entry["name"] = ".."
            entry["isFolder"] = True
            entry["text"] = self.entryFont.render("..", True, self.textColor)
            self.entryList.append(entry)

            self.fileList = os.listdir(os.path.normpath(self.currentPath))
      
            Common.quick_sort(self.fileList)
          
            try:
                for f in self.fileList:                   
                    if(os.path.isdir(self.currentPath + "/" + f)):
                        entry = {}
                        entry["name"] = f
                        entry["isFolder"] = True
                        entry["text"] = None
                        self.entryList.append(entry)
                for f in self.fileList:                   
                    if(not os.path.isdir(self.currentPath + "/" + f) and not self.selectFolder and self.filterFile(f)):
                        entry = {}
                        entry["name"] = f
                        entry["isFolder"] = False
                        entry["text"] = None
                        self.entryList.append(entry)
            except Exception as ex:
                pass    

        if(not self.reset == None):
            for entry in self.entryList:
                if(entry["name"] == self.reset):
                    self.setSelection(self.entryList.index(entry))
        else:
            self.setSelection(0)
        

        self.onChange()
        self.listReady = True
        RenderControl.setDirty()

        


    def getExistingParent(self, path):
        if(path == "/" or path == "" or path == "."):
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

        
    def filterName(self, filename):
        if(not "fileFilter" in self.options):
            return filename

        return os.path.splitext(filename)[0]
        
        

    def filterFile(self, file):
        if(not "fileFilter" in self.options):
            return True #allow all files

        filename, file_extension = os.path.splitext(file)
        if(file_extension == ""):
            return False

        if any(file_extension in s for s in self.options["fileFilter"]):
            return True

        return False
    
    def setInitialSelection(self, index):
        self.setSelection(index)
        self.onChange()            
        self.preview_final = self.previewPath            
        RenderControl.setDirty()
    
  

    def __init__(self, screen, titel, initialPath, selectFolder, options, callback):        
        AbstractList.AbstractList.__init__(self,screen, titel, options)
      
        if(initialPath == None or initialPath == "/"):
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
        self.xFolderOffset = (self.listEntryHeight - self.folderIcon.get_width()) / 2 + 2

        self.yFileOffset =  0
        
        res = ResumeHandler.getResumeFile()
        if(res != None and res["path"] != None):
            self.currentSelection = res["path"]
            self.currentPath = res["path"]
            self.initialPath = res["path"]

        self.initList()
  
        if(res != None and res["line"] != None):           
            self.setInitialSelection(res["line"])
        else:            
            if(os.path.isfile(initialPath) and self.fileList is not None):
                name = ntpath.basename(initialPath)
                index = self.fileList.index(name)
                if(index != -1):
                    self.setInitialSelection(index + 1)      

        if(initialPath == None or initialPath == "/"):
            self.moveFolderUp()
      
