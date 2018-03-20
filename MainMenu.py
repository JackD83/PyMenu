import RenderObject, Configuration, SelectionMenu, FileChooser, EmuRunner, Header, TextInput, ConfigMenu
import Footer, Keys, RenderControl
import os
import pygame, sys
from pprint import pprint

class MainMenu(RenderObject.RenderObject):
    config = Configuration.getConfiguration()
    theme = Configuration.getTheme()
   
    systems = []
    systemNames = []
    systembackgrounds = []
    currentIndex = 0
    inTransition = False
    transitionOffset = 0
    systemOffset = 160
    transitionDirection = 1
    optionsMenu = None
    subComponent = None

  
        
    def loadSystemImages(self, screen):   
        
        pprint(self.config)

        for entry in self.config["mainMenu"]:
            try:
                self.systems.append(pygame.image.load( entry["icon"]))
                self.systembackgrounds.append(pygame.image.load( entry["background"]))
            except ValueError:
                pass

        print("loaded ", len(self.systems), " images" )
        print("loaded ", len(self.systembackgrounds), " backgrounds" )
    
    def handleEvents(self, events):   
        if(self.subComponent != None):
            self.subComponent.handleEvents(events)
            return

        if(self.optionsMenu != None):
            self.optionsMenu.handleEvents(events)
            return

        for event in events:    
            if event.type == pygame.KEYDOWN:           
                if event.key == Keys.DINGOO_BUTTON_LEFT:
                    self.inTransition = True
                    self.transitionDirection = -30
                    RenderControl.setDirty()
                if event.key == Keys.DINGOO_BUTTON_RIGHT:
                    self.inTransition = True
                    self.transitionDirection = 30
                    RenderControl.setDirty()
                if event.key == Keys.DINGOO_BUTTON_SELECT:
                    pass
                    #self.openOptions()
                if event.key == Keys.DINGOO_BUTTON_A:
                    self.openSelection()
                    RenderControl.setDirty()
                if event.key == Keys.DINGOO_BUTTON_START:
                    self.subComponent = ConfigMenu.ConfigMenu(self.screen, "General Options",{"textColor":(255,255,255), "backgroundColor":(0,0,0)}, \
                    {"StringTest":"testString","BooleanTest":"True","FolderTest":"d:\\tmp","FileTest":"d:\\tmp\\test","ImageTest":"d:\\tmp\\image.jpg" }, \
                                                                                                    [{"name":"StringTest","type":"string" }, \
                                                                                                    {"name":"BooleanTest", "type":"boolean"},\
                                                                                                    {"name":"FolderTest", "type":"folder"},\
                                                                                                    {"name":"FileTest", "type":"file"},\
                                                                                                    {"name":"ImageTest", "type":"image"}],\
                                                                                                     self.emulatorCallback)
                    footer = Footer.Footer([("theme/direction.png","select")], [("theme/b_button.png", "back"), ("theme/a_button.png", "change"), ("theme/start_button.png", "save")], (255,255,255)) 
                    self.subComponent.setFooter(footer)             
                    RenderControl.setDirty()                                                                    
    
    def openOptions(self):
        print("opening options menu")
        self.optionsMenu = SelectionMenu.SelectionMenu(self.screen, ["add new entry", "edit entry", "remove entry"], self.optionsCallback)

    def openSelection(self):
        print("Opening selection")
        current = self.config["mainMenu"][self.currentIndex]

        if(current["type"] == "emulator"):
            print("Opening emulator file selection")
            options = {}
            options["background"] = current["background"]
            self.subComponent = FileChooser.FileChooser(self.screen, current["name"], current["selectionPath"], False, options, self.emulatorCallback)

    def optionsCallback(self, optionID):
        print("Options came back with: ", optionID)
        self.optionsMenu = None
    
    def textCallback(self, text):
        print("Text callback, got text: " + text)
        self.subComponent = None

    def emulatorCallback(self, selectedFile):     
        self.subComponent = None
        EmuRunner.runEmu(self.config["mainMenu"][self.currentIndex], selectedFile)

    


    def transition(self):
        if(self.inTransition):
            self.transitionOffset += self.transitionDirection
            if(abs(self.transitionOffset) >= 160):
                self.inTransition = False
                self.transitionOffset = 0
                if(self.transitionDirection < 0):
                    self.currentIndex = self.getNext()
                else:
                    self.currentIndex = self.getPrev()          
           
    
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

        self.transition()

        screen.blit(self.systembackgrounds[self.currentIndex], (0, 0))
        screen.blit(self.banderole, (0,80))

        #current
        screen.blit(self.systems[self.currentIndex], ( (240 - self.systems[self.currentIndex].get_width() / 2) + self.transitionOffset , 40 + 80  -self.systems[self.currentIndex].get_height() / 2 ))

        #previous
        screen.blit(self.systems[self.getPrev()], (0  + self.transitionOffset , 40 + 80  -self.systems[self.getPrev()].get_height() / 2 ))

        #next
        screen.blit(self.systems[self.getNext()], ( (480 - self.systems[self.currentIndex].get_width())  + self.transitionOffset, 40 + 80  -self.systems[self.getNext()].get_height() / 2 ))
        
        self.footer.render(screen)

        self.header.render(screen)

        if(self.optionsMenu != None):
            self.optionsMenu.render(screen)    
        
        if(self.inTransition):
             RenderControl.setInTransition()
        else:
            RenderControl.setInTransition(False)
   
 
    
    def __init__(self, screen):
        print("Main Menu Init")
        self.loadSystemImages(screen)
        self.screen = screen
        self.banderole = pygame.Surface((480,80),pygame.SRCALPHA)
        self.banderole.fill((255,255,255, 160))
      
        self.header = Header.Header(24)
        self.footer = Footer.Footer([("theme/direction.png","select")], [("theme/select_button.png", "options"), ("theme/a_button.png", "open")], (255,255,255))