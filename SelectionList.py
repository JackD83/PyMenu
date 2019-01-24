import RenderObject, Configuration, AbstractList, ConfigMenu, Footer, ConfirmOverlay
import os, Keys, RenderControl, Common, SelectionMenu, FileChooser
import pygame, sys, ResumeHandler, os, copy
import platform
import json
from operator import itemgetter

class SelectionList(AbstractList.AbstractList):
   
    folderIcon = Common.loadImage( "theme/folder.png")
    fileIcon =  Common.loadImage( "theme/file.png")
    overlay = None
    subComponent = None
    options = None
  

  
    currentSelection = None

    def render(self, screen):
        if(self.subComponent != None):
            self.subComponent.render(screen)
            return
        else:       
            AbstractList.AbstractList.render(self, screen)      

        if(self.overlay != None):           
            self.overlay.render(screen)
          
 
    def renderEntry(self, screen, index, xOffset, yOffset):       
        text = self.entryList[index]["text"]
        yTextOffset = (self.listEntryHeight -  text.get_height()) / 2
        screen.blit(text, (4 + xOffset, yOffset + yTextOffset + 1))
  

    def onSelect(self):
        if(self.options["options"][self.currentIndex] in self.data):
            self.data.remove(self.options["options"][self.currentIndex])
        else:
            self.data.append(self.options["options"][self.currentIndex])

        self.initList()
        RenderControl.setDirty()                   
    
    def onExit(self):         
        self.callback(None)    

    def openSelection(self):        
        pass

    

    def onChange(self):
        if(len(self.entryList) == 0):
            self.previewPath = None
            return

       
        elif (len(self.entryList) - 1 < self.currentIndex):
            self.currentIndex = len(self.entryList) - 1

        if(len(self.entryList) == 1):
            self.currentIndex == 0
        

        self.currentSelection = self.entryList[self.currentIndex]
            
       

    def handleEvents(self, events):
        if(self.subComponent != None):
            self.subComponent.handleEvents(events)          
            return


        if(self.overlay != None):
            self.overlay.handleEvents(events)            
            return

        for event in events:    
            if event.type == pygame.KEYDOWN:  
                if event.key == Keys.DINGOO_BUTTON_SELECT:
                    pass
               
            if event.type == pygame.KEYUP:         
                if event.key == Keys.DINGOO_BUTTON_START:
                   self.callback(self.data)
                   return

        if(self.overlay is None):
            AbstractList.AbstractList.handleEvents(self, events)

   
    def initList(self):    
        self.entryList = []
        for idx, o in enumerate(self.options["names"]) :
            entry = {}

            if(self.options["options"][idx] in self.data):
                char = "(X)"
            else:
                char = "( )"

            entry["name"] = o         
            entry["text"] = self.entryFont.render( char + " " + o , True, self.textColor)
            self.entryList.append(entry)
        self.onChange()
   
    

    def __init__(self, screen, titel, data, options, callback):        
        AbstractList.AbstractList.__init__(self, screen, titel, options)

        if(data == None):
            data = []
                 
        self.options = options
        self.callback = callback
        self.data = data

        self.yFolderOffset = (self.listEntryHeight - self.folderIcon.get_height()) / 2
        self.xFolderOffset = (self.listEntryHeight - self.folderIcon.get_width()) / 2

        self.yFileOffset =  (self.listEntryHeight - self.fileIcon.get_height()) / 2
        self.xFileOffset =  (self.listEntryHeight - self.fileIcon.get_width()) / 2

        self.initList()

                  
      
      