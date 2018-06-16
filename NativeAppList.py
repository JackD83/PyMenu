import RenderObject, Configuration, AbstractList, ConfigMenu, Footer, ConfirmOverlay
import os, Keys, RenderControl, Common, SelectionMenu
import pygame, sys, ResumeHandler
import platform
import json
from operator import itemgetter

class NativeAppList(AbstractList.AbstractList):
   
    folderIcon = Common.loadImage( "theme/folder.png")
    fileIcon =  Common.loadImage( "theme/file.png")
    overlay = None
    subComponent = None
  

    configOptions = [
    {   "id":"cmd",
        "name" :"Executable",
        "type":"file"
    }, 
    {
        "id":"name",
        "name" :"Name",
        "type":"string",        
    },      
    {   "id":"preview",
        "name" :"Preview Image",
        "type":"image"      
    },     
    {   "id":"screen",
        "name" :"Screen option",
        "type":"list",
        "values": ["default", "fullscreen", "center"]      
    },     
    {   "id":"overclock",
        "name" :"Overclock",
        "type":"list",
        "values": ["528", "552", "576","600", "624"]
    }
    ]

    previewCache = {}
    previewEnabled = True
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
        if(len(self.entryList) > 0):
            ResumeHandler.setLastSelectedLine(self.currentIndex)
            self.callback(self.entryList[self.currentIndex]["options"])
    
    def onExit(self):
        print("exit") 
        self.callback(None)    
    
    def onChange(self):
        if(len(self.entryList) == 0):
            self.previewPath = None
            self.previewEnabled = False
            return

        if(len(self.entryList) - 1 < self.currentIndex):
            self.currentIndex = len(self.entryList) - 1

        self.currentSelection = self.entryList[self.currentIndex]["options"]
        self.previewPath = self.currentSelection["preview"]
        
       

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
                    if(len(self.options) == 0):
                        self.overlay = SelectionMenu.SelectionMenu(self.screen, ["add"], self.optionsCallback)
                    else:
                         self.overlay = SelectionMenu.SelectionMenu(self.screen, ["add", "edit", "remove"], self.optionsCallback)
                    RenderControl.setDirty()

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

        if(not Configuration.isRS97()):
            self.configOptions = self.configOptions + json.load(open('config/legacy.json'))
          
     
        if(selection == 0):
            self.subComponent = ConfigMenu.ConfigMenu(self.screen, "Add new link",{"textColor":(55,55,55), "backgroundColor":(221,221,221)}, \
                                        self.getEmptyData() ,self.configOptions ,self.addEditCallback)
            footer = Footer.Footer([("theme/direction.png","select")], [("theme/b_button.png", "back"), ("theme/a_button.png", "change"), ("theme/start_button.png", "save")], (255,255,255)) 
            self.subComponent.setFooter(footer)
            self.subComponent.setConfigCallback(self.configCallback)
        if(selection == 1):
            self.subComponent = ConfigMenu.ConfigMenu(self.screen, "Edit link",{"textColor":(55,55,55), "backgroundColor":(221,221,221)}, \
                                        self.currentSelection ,self.configOptions ,self.addEditCallback)
            footer = Footer.Footer([("theme/direction.png","select")], [("theme/b_button.png", "back"), ("theme/a_button.png", "change"), ("theme/start_button.png", "save")], (255,255,255)) 
            self.subComponent.setFooter(footer)
            self.subComponent.setConfigCallback(self.configCallback)
        if(selection == 2):
            self.overlay = ConfirmOverlay.ConfirmOverlay("really delete?", (255,255,255),  [("theme/b_button.png", "back"), ("theme/a_button.png", "delete")], self.deleteCallback)
            RenderControl.setDirty()  
         

    def deleteCallback(self, res):
        self.overlay = None
        if(res == 1):            
            self.data.remove(self.currentSelection)
            Configuration.saveConfiguration()          
            self.initList()
            self.setSelection(self.currentSelection - 1)            
            

    def addEditCallback(self, configCallback):        
        if(configCallback != None and not configCallback in self.data):
            self.data.append(configCallback)            
   
        Configuration.saveConfiguration()            
        self.subComponent = None
        self.initList()
        self.setSelection(len(self.entryList) - 1)
       

    def configCallback(self, config):
        if(config["name"] == None and ( config["cmd"] != None or config["cmd"] == "None" )   ):
            name = os.path.basename(config["cmd"])
            name = os.path.splitext(name)[0]
            config["name"] = name
    

    def getEmptyData(self):
        emptyEntry = {
            "name": None,
            "cmd":".",
            "icon":".",
            "preview":".",
            "legacy":False,
            "screen":"default",
            "overclock":"528"
        }
        return emptyEntry


    def __init__(self, screen, titel, data, options, callback):        
        AbstractList.AbstractList.__init__(self, screen, titel, options)
                 
   
        self.callback = callback
        self.data = data

        self.yFolderOffset = (self.listEntryHeight - self.folderIcon.get_height()) / 2
        self.xFolderOffset = (self.listEntryHeight - self.folderIcon.get_width()) / 2

        self.yFileOffset =  (self.listEntryHeight - self.fileIcon.get_height()) / 2
        self.xFileOffset =  (self.listEntryHeight - self.fileIcon.get_width()) / 2

        self.initList()

        res = ResumeHandler.getResumeFile()
        if(res != None):
            self.setSelection(res["line"])

        
      
      