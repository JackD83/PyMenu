import RenderObject, Configuration, AbstractList, TextInput,SelectionMenu,FileChooser, Footer
import os, RenderControl
import pygame, sys
from operator import itemgetter

class ConfigMenu(AbstractList.AbstractList):
    subComponent = None
    optionsMenu = None
    footer = None
     
    def render(self, screen):
        if(self.subComponent != None):
            self.subComponent.render(screen)
            return
        else:            
            super().render(screen)

        if(self.optionsMenu != None):
            self.optionsMenu.render(screen)
     
    def renderEntry(self, screen, index, yOffset):
        text = self.entryList[index]["text"]
        yTextOffset = (self.listEntryHeight -  text.get_height()) / 2
        screen.blit(text, (4, yOffset + yTextOffset + 1))
      

    def onSelect(self):
        print("on select")
        if(self.entryList[self.currentIndex]["type"] == "string"):
            self.subComponent = TextInput.TextInput(self.screen, self.entryList[self.currentIndex]["value"], self.textCallback)
            footer = Footer.Footer([("theme/direction.png","select")], [("theme/b_button.png", "back"), ("theme/a_button.png", "add"), ("theme/start_button.png", "save")], (255,255,255)) 
            self.subComponent.setFooter(footer)          
        if(self.entryList[self.currentIndex]["type"] == "boolean"):
           self.optionsMenu = SelectionMenu.SelectionMenu(self.screen, ["True", "False"], self.booleanCallback)
        if(self.entryList[self.currentIndex]["type"] == "folder"):
            options = {}   
            options["preview"] = False        
            self.subComponent = FileChooser.FileChooser(self.screen, self.entryList[self.currentIndex]["name"] ,self.entryList[self.currentIndex]["value"], True, options, self.fileFolderCallback)
            footer = Footer.Footer([("theme/direction.png","select")], [("theme/b_button.png", "back"), ("theme/a_button.png", "enter"), ("theme/start_button.png", "save")], (255,255,255)) 
            self.subComponent.setFooter(footer)       
        if(self.entryList[self.currentIndex]["type"] == "file"):
            options = {}   
            options["preview"] = False        
            self.subComponent = FileChooser.FileChooser(self.screen, self.entryList[self.currentIndex]["name"] ,self.entryList[self.currentIndex]["value"], False, options, self.fileFolderCallback)
            footer = Footer.Footer([("theme/direction.png","select")], [("theme/b_button.png", "back"), ("theme/a_button.png", "select")], (255,255,255)) 
            self.subComponent.setFooter(footer) 
        if(self.entryList[self.currentIndex]["type"] == "image"):
            options = {}   
            options["preview"] = True
            options["directPreview"] = True 
            options["fileFilter"] = [".png", ".jpg"] 
            options["textColor"] = self.textColor
            options["backgroundColor"] = self.backgroundColor
            self.subComponent = FileChooser.FileChooser(self.screen, self.entryList[self.currentIndex]["name"] ,self.entryList[self.currentIndex]["value"], False, options, self.fileFolderCallback)
            footer = Footer.Footer([("theme/direction.png","select")], [("theme/b_button.png", "back"), ("theme/a_button.png", "select")], (255,255,255)) 
            self.subComponent.setFooter(footer)       

    def textCallback(self, text):      
        print("Got new text for: " + self.entryList[self.currentIndex]["name"]  + ": " + text)
        self.optionTarget[self.entryList[self.currentIndex]["name"]] = text
        self.initList()
        self.subComponent = None

    def booleanCallback(self, selection):
        self.optionsMenu = None     

        text = "True"
        if(selection == 1):
            text = "False"

        print("Got new boolean for: " + self.entryList[self.currentIndex]["name"] + ": " + text)
        self.optionTarget[self.entryList[self.currentIndex]["name"]] = text
        self.initList()

    def fileFolderCallback(self, folder):
        self.subComponent = None
        print("File/Folder selected: " + folder)
        self.optionTarget[self.entryList[self.currentIndex]["name"]] = folder
        self.initList()

    
    def onExit(self):
        self.callback(None)

    def handleEvents(self, events):
        if(self.subComponent != None):
            self.subComponent.handleEvents(events)          
            return

        if(self.optionsMenu != None):
            self.optionsMenu.handleEvents(events)           
            return

        if(self.optionsMenu == None and self.subComponent == None):
            super().handleEvents(events)
           
   
    def initList(self):
        self.entryList = []
        for o in self.optionConfig:
            entry = {}
            entry["name"] = o["name"]
            entry["value"] = self.optionTarget[o["name"]]
            entry["type"] = o["type"]
            entry["text"] = self.entryFont.render( entry["name"] + ": " + entry["value"] , True, self.textColor)
            self.entryList.append(entry)

    def __init__(self, screen, titel,  options, optionTarget, optionConfig, callback):
        super().__init__(screen, titel, options)
        self.callback = callback
        self.optionConfig = optionConfig
        self.optionTarget = optionTarget
           
        
        self.initList()