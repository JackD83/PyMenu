import RenderObject, Configuration, AbstractList, TextInput,SelectionMenu,FileChooser, Footer
import os, RenderControl, Keys
import pygame, sys, ntpath

from operator import itemgetter

class ConfigMenu(AbstractList.AbstractList):
    subComponent = None
    overlay = None
    footer = None
    configCallback = None

    originalTarget = None

    def render(self, screen):
        if(self.subComponent != None):
            self.subComponent.render(screen)
            return
        else:            
            AbstractList.AbstractList.render(self,screen)

        if(self.overlay != None):
            self.overlay.render(screen)
     
    def renderEntry(self, screen, index, xOffset, yOffset):
        text = self.entryList[index]["text"]
        yTextOffset = (self.listEntryHeight -  text.get_height()) / 2
        screen.blit(text, (4 + xOffset , yOffset + yTextOffset + 1))
    
    def setConfigCallback(self, callback):
        self.configCallback = callback
      

    def onSelect(self):        
        if(self.entryList[self.currentIndex]["type"] == "string"):
            self.subComponent = TextInput.TextInput(self.screen, self.entryList[self.currentIndex]["value"], self.textCallback)
            footer = Footer.Footer([("theme/direction.png","select")], [("theme/b_button.png", "back"), ("theme/a_button.png", "add"), ("theme/start_button.png", "save")], (255,255,255)) 
            self.subComponent.setFooter(footer)          
        if(self.entryList[self.currentIndex]["type"] == "boolean"):
           self.overlay = SelectionMenu.SelectionMenu(self.screen, ["True", "False"], self.booleanCallback)
        if(self.entryList[self.currentIndex]["type"] == "folder"):
            options = {}   
            options["preview"] = False        
            self.subComponent = FileChooser.FileChooser(self.screen, self.entryList[self.currentIndex]["name"] ,self.entryList[self.currentIndex]["value"], True, options, self.fileFolderCallback)
            footer = Footer.Footer([("theme/direction.png","select")], [("theme/b_button.png", "back"), ("theme/a_button.png", "enter"), ("theme/start_button.png", "save")], (255,255,255)) 
            self.subComponent.setFooter(footer)       
        if(self.entryList[self.currentIndex]["type"] == "file"):
            options = {}   
            options["preview"] = False  

            if("filter" in self.entryList[self.currentIndex]["options"]):
                options["fileFilter"] = self.entryList[self.currentIndex]["options"]["filter"]

            self.subComponent = FileChooser.FileChooser(self.screen, self.entryList[self.currentIndex]["name"] ,self.entryList[self.currentIndex]["value"], False, options, self.fileFolderCallback)
            footer = Footer.Footer([("theme/direction.png","select")], [("theme/b_button.png", "back"), ("theme/a_button.png", "select")], (255,255,255)) 
            self.subComponent.setFooter(footer) 
        if(self.entryList[self.currentIndex]["type"] == "image"):
            options = {}   
            options["preview"] = True
            options["useSidebar"] = True
            options["directPreview"] = True 
            options["fileFilter"] = [".png", ".jpg"] 
            options["textColor"] = self.textColor
            options["backgroundColor"] = self.backgroundColor
            self.subComponent = FileChooser.FileChooser(self.screen, self.entryList[self.currentIndex]["name"] ,self.entryList[self.currentIndex]["value"], False, options, self.fileFolderCallback)
            footer = Footer.Footer([("theme/direction.png","select")], [("theme/b_button.png", "back"), ("theme/a_button.png", "select")], (255,255,255)) 
            self.subComponent.setFooter(footer)
        if(self.entryList[self.currentIndex]["type"] == "list"):   
            if("names" in self.entryList[self.currentIndex]["options"]):
                self.overlay = SelectionMenu.SelectionMenu(self.screen, self.entryList[self.currentIndex]["options"]["names"], self.listCallback)
            else:
                self.overlay = SelectionMenu.SelectionMenu(self.screen, self.entryList[self.currentIndex]["options"]["values"], self.listCallback)

    def textCallback(self, text):      
        if(text == None):
            text = self.optionTarget[self.entryList[self.currentIndex]["id"]]

        print("Got new text for: " + self.entryList[self.currentIndex]["id"]  + ": " + text)
        self.optionTarget[self.entryList[self.currentIndex]["id"]] = text
        self.fireConfigChanged()
        self.initList()
        self.subComponent = None
       

    def booleanCallback(self, selection, text):
        self.overlay = None     

        text = "True"
        if(selection == 1):
            text = "False"
       
        self.optionTarget[self.entryList[self.currentIndex]["id"]] = text
        self.fireConfigChanged()
        self.initList()
      

    def fileFolderCallback(self, folder):
        if(folder == None):
            folder =  self.optionTarget[self.entryList[self.currentIndex]["id"]]

        self.subComponent = None
        print("File/Folder selected: " + str(folder))
        self.optionTarget[self.entryList[self.currentIndex]["id"]] = str(folder)
        self.fireConfigChanged()
        self.initList()
       

    def listCallback(self, selection, text):
        self.overlay = None
        self.optionTarget[self.entryList[self.currentIndex]["id"]] = self.entryList[self.currentIndex]["options"]["values"][selection]
        self.fireConfigChanged()
        self.initList()
    
    def fireConfigChanged(self):
        if(self.configCallback != None):
            self.configCallback(self.optionTarget)
       

    def onChange(self):

        if("description" in self.entryList[self.currentIndex]["options"]):
            self.options["description"] = self.entryList[self.currentIndex]["options"]["description"]            
        else:
            self.options["description"] = ""
        self.initHeader()

        if(self.entryList[self.currentIndex]["type"] == "image"): 
            #self.previewEnabled = True      
            self.previewPath = self.entryList[self.currentIndex]["value"]
        else:
            self.previewEnabled = False   
            self.previewPath = None

        
    def onExit(self):
        self.callback(None)

    def handleEvents(self, events):
        if(self.subComponent != None):
            self.subComponent.handleEvents(events)          
            return

        if(self.overlay != None):
            self.overlay.handleEvents(events)           
            return

        for event in events:    
            if event.type == pygame.KEYDOWN:
                if event.key == Keys.DINGOO_BUTTON_Y:                  
                    self.toggleSidebar(True)
            if event.type == pygame.KEYUP:         
                if event.key == Keys.DINGOO_BUTTON_START:  
                    self.originalTarget.update(self.optionTarget)

                    self.callback(self.originalTarget)
                    RenderControl.setDirty()
                  

        if(self.overlay == None and self.subComponent == None):
            AbstractList.AbstractList.handleEvents(self,events)
           
   
    def initList(self):
        self.entryList = []
        for o in self.optionConfig:
            if(not o["id"] in self.optionTarget):
                self.optionTarget[o["id"]] = None


            entry = {}
            entry["options"] = o
            entry["name"] = o["name"]
            entry["id"] = o["id"]           
            entry["type"] = o["type"]

            entry["value"] = self.optionTarget[o["id"]]

            if("names" in o and "values" in o and entry["value"] in o["values"]):
                entry["text"] = self.entryFont.render( entry["name"] + ": " + str(o["names"][o["values"].index(entry["value"])]) , True, self.textColor)
            else:      
                entry["text"] = self.entryFont.render( entry["name"] + ": " + ntpath.basename(str(entry["value"])) , True, self.textColor)

            self.entryList.append(entry)
        self.onChange()

    def __init__(self, screen, titel,  options, optionTarget, optionConfig, callback):
        AbstractList.AbstractList.__init__(self, screen, titel, options)
        self.callback = callback
      

        self.optionConfig = optionConfig
        self.optionTarget = optionTarget.copy()
        self.originalTarget = optionTarget
        self.previewEnabled = False  
        self.toggleSidebar(False)    
        self.initList()
      