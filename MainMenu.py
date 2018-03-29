import RenderObject, Configuration, SelectionMenu, FileChooser, Runner, Header, TextInput, ConfigMenu
import Footer, Keys, RenderControl, InfoOverlay, Common, NativeAppList,TaskHandler
import os
import json
import pygame, sys
from pprint import pprint

class MainMenu(RenderObject.RenderObject):
    config = Configuration.getConfiguration()
    theme = Configuration.getTheme()

   
    header = None
    footer = None
    systems = []
    systemNames = []
    systembackgrounds = []
    currentIndex = 0
    inTransition = False
    transitionOffset = 0
    systemOffset = 160
   
    overlay = None
    subComponent = None
        
    def loadSystemImages(self, screen):           
        pprint(self.config)
        for entry in self.config["mainMenu"]:
            try:
                self.systems.append(Common.loadImage( entry["icon"]))
                self.systembackgrounds.append(Common.loadImage( entry["background"]))
            except ValueError:
                pass

        print("loaded ", len(self.systems), " images" )
        print("loaded ", len(self.systembackgrounds), " backgrounds" )
    
    def handleEvents(self, events):   
        if(self.subComponent != None):
            self.subComponent.handleEvents(events)
            return

        if(self.overlay != None):
            self.overlay.handleEvents(events)
            return

        for event in events:    
            if event.type == pygame.KEYDOWN:           
                if event.key == Keys.DINGOO_BUTTON_LEFT:
                    if(not self.inTransition):
                        TaskHandler.addAnimation(0, -160, 200, self.transitionCallback)
                        self.inTransition = True             
                        RenderControl.setDirty()
                if event.key == Keys.DINGOO_BUTTON_RIGHT:
                    if(not self.inTransition):
                        TaskHandler.addAnimation(0, 160,200, self.transitionCallback)
                        self.inTransition = True             
                        RenderControl.setDirty()
                if event.key == Keys.DINGOO_BUTTON_SELECT:                    
                    self.openOptions()
                    RenderControl.setDirty()
                if event.key == Keys.DINGOO_BUTTON_A:
                    self.openSelection()
                    RenderControl.setDirty()
                if event.key == Keys.DINGOO_BUTTON_START:
                    pass

    def transitionCallback(self, start, target, current, finished):
        if(finished):
            self.inTransition = False
            self.transitionOffset = 0
            if(target < 0):
                self.currentIndex = self.getNext()
            else:
                self.currentIndex = self.getPrev()
        else:
            self.transitionOffset = current
            
        RenderControl.setDirty()

    
    def openOptions(self):
        print("opening options menu")
        self.overlay = SelectionMenu.SelectionMenu(self.screen, ["add new entry", "edit entry", "remove entry"], self.optionsCallback)

    def openSelection(self):
        print("Opening selection")
        current = self.config["mainMenu"][self.currentIndex]

        if(current["type"] == "emulator"):
            print("Opening emulator file selection")
            options = {}
            options["background"] = current["background"]
            
            if("previews" in current):
                options["previews"] = current["previews"]
            
            if("fileFilter" in current):
                options["fileFilter"] = current["fileFilter"]

            self.subComponent = FileChooser.FileChooser(self.screen, current["name"], current["selectionPath"], False, options, self.emulatorCallback)
        
        if(current["type"] == "config"):
            self.subComponent = ConfigMenu.ConfigMenu(self.screen, "General Options",{"textColor":(255,255,255), "backgroundColor":(0,0,0)}, \
                                        Configuration.getPathData(current["data"]), json.load(open(current["config"])) ,self.emulatorCallback)
            footer = Footer.Footer([("theme/direction.png","select")], [("theme/b_button.png", "back"), ("theme/a_button.png", "change"), ("theme/start_button.png", "save")], (255,255,255)) 
            self.subComponent.setFooter(footer)    
                     
        if(current["type"] == "native"):
            print("Opening native selection")
            options = {}
            options["background"] = current["background"]
            self.subComponent = NativeAppList.NativeAppList(self.screen, current["name"], current["data"] , options, self.nativeCallback)
            footer = Footer.Footer([("theme/direction.png","select")], [("theme/b_button.png", "back"), ("theme/a_button.png", "select"), ("theme/select_button.png", "options")], (255,255,255)) 
            self.subComponent.setFooter(footer)    

    def nativeCallback(self, selection):
        self.subComponent = None
        if(selection != None):
            Runner.runNative(selection)


    def optionsCallback(self, optionID):
        print("Options came back with: ", optionID)
        self.overlay = None
    
    def textCallback(self, text):
        print("Text callback, got text: " + text)
        self.subComponent = None

    def emulatorCallback(self, selectedFile):     
        self.subComponent = None
        if(selectedFile != None):
            Runner.runEmu(self.config["mainMenu"][self.currentIndex], selectedFile)

    def infoCallback(self, res):
        self.overlay = None
        
        self.config["firstStart"] = False
        Configuration.saveConfiguration()
    
    
    def getNext(self):     
        if(self.currentIndex + 1 >= len(self.systems)):
            return 0
        else:
            return self.currentIndex + 1

    def getPrev(self):       
        if(self.currentIndex - 1 < 0):
            return len(self.systems) - 1
        else:
            return self.currentIndex -1
        

    def render(self, screen):
        if(self.subComponent != None):
            self.subComponent.render(screen)
            return     

        screen.blit(self.systembackgrounds[self.currentIndex], (0, 0))
        screen.blit(self.banderole, (0,80))

        #current
        screen.blit(self.systems[self.currentIndex], ( (240 - self.systems[self.currentIndex].get_width() / 2) + self.transitionOffset , 40 + 80  -self.systems[self.currentIndex].get_height() / 2 ))

        #previous
        screen.blit(self.systems[self.getPrev()], (0  + self.transitionOffset , 40 + 80  -self.systems[self.getPrev()].get_height() / 2 ))

        #next
        screen.blit(self.systems[self.getNext()], ( (480 - self.systems[self.currentIndex].get_width())  + self.transitionOffset, 40 + 80  -self.systems[self.getNext()].get_height() / 2 ))
        
        if(self.footer != None):
            self.footer.render(screen)

        self.header.render(screen)

        if(self.overlay != None):
            self.overlay.render(screen)    
            
   
 
    
    def __init__(self, screen):
        print("Main Menu Init")
        self.loadSystemImages(screen)
        self.screen = screen
        self.banderole = pygame.Surface((480,80),pygame.SRCALPHA)
        self.banderole.fill((255,255,255, 160))
      
        self.header = Header.Header(24)

        if("firstStart" in self.config and self.config["firstStart"]):
             self.overlay = InfoOverlay.InfoOverlay("theme/info.png", self.infoCallback)

        #self.footer = Footer.Footer([("theme/direction.png","select")], [("theme/select_button.png", "options"), ("theme/a_button.png", "open")], (255,255,255))