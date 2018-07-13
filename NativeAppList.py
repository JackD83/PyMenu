import RenderObject, Configuration, AbstractList, ConfigMenu, Footer, ConfirmOverlay
import os, Keys, RenderControl, Common, SelectionMenu, FileChooser
import pygame, sys, ResumeHandler, os
import platform
import json
from operator import itemgetter

class NativeAppList(AbstractList.AbstractList):
   
    folderIcon = Common.loadImage( "theme/folder.png")
    fileIcon =  Common.loadImage( "theme/file.png")
    overlay = None
    subComponent = None
  

    configOptions = json.load(open('config/optionsNative.json'))

    previewCache = {}

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
            print(self.entryList[self.currentIndex]["options"] )
            if("selector" in self.entryList[self.currentIndex]["options"] and self.entryList[self.currentIndex]["options"]["selector"]):              
                self.openSelection()
            else:
                ResumeHandler.setLastSelectedLine(self.currentIndex)
                self.callback(self.entryList[self.currentIndex]["options"])                    
    
    def onExit(self):
        print("exit") 
        self.callback(None)    

    def openSelection(self):
        print("Opening file selection")
        options = {}
        options["textColor"] = (55,55,55)
        options["background"] = self.options["background"]
        options["useSidebar"] = False

        if("selectDescription" in self.entryList[self.currentIndex]["options"]):
            options["description"] =  self.entryList[self.currentIndex]["options"]["selectDescription"]

        if("folderIcon" in  self.options):
            options["folderIcon"] =  self.options["folderIcon"]
              
        
        if("fileFilter" in  self.entryList[self.currentIndex]["options"]):
            options["fileFilter"] = self.entryList[self.currentIndex]["options"]

        if("selectionPath" in self.entryList[self.currentIndex]["options"]):
            selectionPath = self.entryList[self.currentIndex]["options"]
        else:
            selectionPath = "/"

        print(options)


        self.subComponent = FileChooser.FileChooser(self.screen,self.entryList[self.currentIndex]["options"]["name"], selectionPath, False, options, self.selectionCallback)
        footer = Footer.Footer([("theme/direction.png","select")], [("theme/b_button.png", "back"), ("theme/a_button.png", "select")], (255,255,255)) 
        self.subComponent.setFooter(footer)

    def selectionCallback(self, selection):      
        self.subComponent = None

        if(selection is not None):
            self.entryList[self.currentIndex]["options"]["selection"] = selection
            ResumeHandler.setLastSelectedLine(self.currentIndex)
            self.callback(self.entryList[self.currentIndex]["options"])

    
    def onChange(self):
        if(len(self.entryList) == 0):
            self.previewPath = None
         
            return

        if(len(self.entryList) - 1 < self.currentIndex):
            self.currentIndex = len(self.entryList) - 1

        self.currentSelection = self.entryList[self.currentIndex]["options"]

        if(os.path.isfile(self.currentSelection["preview"])):
            self.previewPath = self.currentSelection["preview"]
        else:
            self.previewPath = None

        if("description" in self.currentSelection):           
            self.entryDescription = self.currentSelection["description"]
        else:
            self.entryDescription = None
            
       

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
            self.subComponent = ConfigMenu.ConfigMenu(self.screen, "Add new link",{"textColor":(55,55,55), "backgroundColor":(221,221,221), "useSidebar":True}, \
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
            self.setSelection(self.currentIndex - 1)            
            

    def addEditCallback(self, configCallback):        
        if(configCallback != None and not configCallback in self.data):
            self.data.append(configCallback)            
   
        Configuration.saveConfiguration()            
        self.subComponent = None
        self.initList()
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
        if(res != None and res["line"] != None):
            self.setSelection(res["line"])
            self.onChange()
            self.previewPath = self.currentSelection["preview"]
            self.preview_final = self.previewPath
            RenderControl.setDirty()           
      
      