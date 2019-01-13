import RenderObject, Configuration, AbstractList, ConfigMenu, Footer, ConfirmOverlay
import os, Keys, RenderControl, Common, SelectionMenu, FileChooser
import pygame, sys, ResumeHandler, os
import platform
import json
from operator import itemgetter

class EmulatorList(AbstractList.AbstractList):
   
    folderIcon = Common.loadImage( "theme/folder.png")
    fileIcon =  Common.loadImage( "theme/file.png")
    overlay = None
    subComponent = None
    options = None
  

    configOptions = json.load(open('config/optionsEmulator.json'))

  
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
       pass                    
    
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
        

        self.currentSelection = self.entryList[self.currentIndex]["options"]
            
       

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
                
                    if(len(self.data) == 0):
                        self.overlay = SelectionMenu.SelectionMenu(self.screen, ["add"], self.optionsCallback)
                    else:
                        self.overlay = SelectionMenu.SelectionMenu(self.screen, ["add", "edit", "remove"], self.optionsCallback)
                    RenderControl.setDirty()
            if event.type == pygame.KEYUP:         
                if event.key == Keys.DINGOO_BUTTON_START:
                   self.callback(self.data)
                   return

        if(self.overlay is None):
            AbstractList.AbstractList.handleEvents(self, events)

   
    def initList(self):    
        self.entryList = []
        for o in self.data:
            entry = {}
            entry["options"] = o
            entry["name"] = o["name"]           
            entry["text"] = self.entryFont.render( entry["name"] , True, self.textColor)
            self.entryList.append(entry)
        self.onChange()
   
    def optionsCallback(self, selection, text):           
        self.overlay = None
          
     
        if(text == "add"):
            self.subComponent = ConfigMenu.ConfigMenu(self.screen, "Add new emulator",{"textColor":(55,55,55), "backgroundColor":(221,221,221), "useSidebar":True}, \
                                        self.getEmptyData() ,self.configOptions ,self.addEditCallback)
            footer = Footer.Footer([("theme/direction.png","select")], [("theme/b_button.png", "back"), ("theme/a_button.png", "change"), ("theme/start_button.png", "save")], (255,255,255)) 
            self.subComponent.setFooter(footer)
            self.subComponent.setConfigCallback(self.configCallback)
        if(text == "edit"):
            self.subComponent = ConfigMenu.ConfigMenu(self.screen, "Edit emulator",{"textColor":(55,55,55), "backgroundColor":(221,221,221)}, \
                                        self.currentSelection ,self.configOptions ,self.addEditCallback)
            footer = Footer.Footer([("theme/direction.png","select")], [("theme/b_button.png", "back"), ("theme/a_button.png", "change"), ("theme/start_button.png", "save")], (255,255,255)) 
            self.subComponent.setFooter(footer)
            self.subComponent.setConfigCallback(self.configCallback)
        if(text == "remove"):
            self.overlay = ConfirmOverlay.ConfirmOverlay("really delete?", (255,255,255),  [("theme/b_button.png", "back"), ("theme/a_button.png", "delete")], self.deleteCallback)
            RenderControl.setDirty()
      
         

    def deleteCallback(self, res):
        self.overlay = None
        if(res == 1):            
            self.data.remove(self.currentSelection)
          
            self.initList()


    def addEditCallback(self, configCallback):        
        if(configCallback != None and not configCallback in self.data):
            self.data.append(configCallback)            
     
        self.subComponent = None
        self.initList()
       

        if(self.currentIndex == -1):
            self.setSelection(0)
        else:
            self.setSelection(self.currentIndex)
       

    def configCallback(self, config):
        if(config["name"] == None and ( config["cmd"] != None or config["cmd"] == "None" )   ):
            name = os.path.basename(config["cmd"])
            name = os.path.splitext(name)[0]
            config["name"] = name
        
       
    

    def getEmptyData(self):
        emptyEntry = {
            "name": None,
            "cmd":".",
            "workingDir":"."
           
        }
        return emptyEntry


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

                  
      
      