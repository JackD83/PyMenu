import RenderObject, Configuration, AbstractList, ConfigMenu, Footer
import os, Keys, RenderControl, Common, SelectionMenu
import pygame, sys
from operator import itemgetter

class NativeAppList(AbstractList.AbstractList):
   
    folderIcon = Common.loadImage( "theme/folder.png")
    fileIcon =  Common.loadImage( "theme/file.png")
    overlay = None
    subComponent = None
  

    configOptions = [{
        "id":"name",
        "name" :"Name",
        "type":"string",        
    },
    {   "id":"exe",
        "name" :"Executable",
        "type":"file",
        "filter": [".dge", ".sh"]
    },   
    {   "id":"preview",
        "name" :"Preview Image",
        "type":"image"      
    },     
    {   "id":"legacy",
        "name" :"Legacy app",
        "type":"boolean"      
    },     
    {   "id":"screen",
        "name" :"Screen option",
        "type":"list",
        "values": ["default", "fullscreen", "center"]      
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
            super().render(screen)      

        if(self.overlay != None):
            self.overlay.render(screen)
          
 
    def renderEntry(self, screen, index, yOffset):
        text = self.entryList[index]["text"]
        yTextOffset = (self.listEntryHeight -  text.get_height()) / 2
        screen.blit(text, (4, yOffset + yTextOffset + 1))
  

    def onSelect(self):     
        #TODO   
        self.callback("blaa")
    
    def onExit(self):
        print("exit") 
        self.callback(None)    
    
    def onChange(self):
        if(len(self.entryList) == 0):
            self.previewPath = None
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

        super().handleEvents(events)

   
    def initList(self):
        self.entryList = []
        for o in self.data:
            entry = {}
            entry["options"] = o
            entry["name"] = o["name"]           
            entry["text"] = self.entryFont.render( entry["name"] , True, self.textColor)
            self.entryList.append(entry)
        self.onChange()
   
    def optionsCallback(self, selection):           
        self.overlay = None
     

        if(selection == 0):
            self.subComponent = ConfigMenu.ConfigMenu(self.screen, "Add new link",{"textColor":(255,255,255), "backgroundColor":(0,0,0)}, \
                                        self.getEmptyData() ,self.configOptions ,self.addEditCallback)
            footer = Footer.Footer([("theme/direction.png","select")], [("theme/b_button.png", "back"), ("theme/a_button.png", "change"), ("theme/start_button.png", "save")], (255,255,255)) 
            self.subComponent.setFooter(footer)
        if(selection == 1):
            self.subComponent = ConfigMenu.ConfigMenu(self.screen, "Edit link",{"textColor":(255,255,255), "backgroundColor":(0,0,0)}, \
                                        self.currentSelection ,self.configOptions ,self.addEditCallback)
            footer = Footer.Footer([("theme/direction.png","select")], [("theme/b_button.png", "back"), ("theme/a_button.png", "change"), ("theme/start_button.png", "save")], (255,255,255)) 
            self.subComponent.setFooter(footer)
        if(selection == 2):
            self.data.remove(self.currentSelection)
            Configuration.saveConfiguration()
            self.initList()
         


    def addEditCallback(self, configCallback):
        print("config came back" + str(configCallback))
        if(configCallback != None and not configCallback in self.data):
            self.data.append(configCallback)

        Configuration.saveConfiguration()            
        self.subComponent = None
        self.initList()

    

    def getEmptyData(self):
        emptyEntry = {
            "name": "NewName",
            "exe":"",
            "icon":"",
            "preview":"",
            "legacy":False,
            "screen":"default"
        }
        return emptyEntry


    def __init__(self, screen, titel, data, options, callback):        
        super().__init__(screen, titel, options)
                 
   
        self.callback = callback
        self.data = data

        self.yFolderOffset = (self.listEntryHeight - self.folderIcon.get_height()) / 2
        self.xFolderOffset = (self.listEntryHeight - self.folderIcon.get_width()) / 2

        self.yFileOffset =  (self.listEntryHeight - self.fileIcon.get_height()) / 2
        self.xFileOffset =  (self.listEntryHeight - self.fileIcon.get_width()) / 2

        self.initList()
      
      