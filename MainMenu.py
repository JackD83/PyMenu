import RenderObject, Configuration, SelectionMenu, FileChooser, EmuRunner, Header, TextInput
import os
import pygame, sys
from pprint import pprint

class MainMenu(RenderObject.RenderObject):
    config = Configuration.getConfiguration()
    theme = Configuration.getTheme()
    footerFont = pygame.font.Font('theme/FreeSans.ttf', 14)
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

    footerHeight = 24
        
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
                if event.key == pygame.K_LEFT:
                    self.inTransition = True
                    self.transitionDirection = -30
                if event.key == pygame.K_RIGHT:
                    self.inTransition = True
                    self.transitionDirection = 30
                if event.key == pygame.K_LCTRL:
                    self.openOptions()
                if event.key == pygame.K_RETURN:
                    self.openSelection()
                if event.key == pygame.K_RALT:
                    self.subComponent = TextInput.TextInput(self.screen, "Initial", self.textCallback)
    
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

    def initFooter(self):
        self.footer = pygame.Surface((self.config["screenWidth"], self.footerHeight),pygame.SRCALPHA)
        self.footer.fill(Configuration.toColor(self.theme["footer"]["color"]))
        aButton = pygame.image.load("theme/a_button.png")
        self.footer.blit(aButton, (370,3))
        open = self.footerFont.render("open", True, (255,255,255))
        self.footer.blit(open, (394,3))
        selectButton = pygame.image.load("theme/select_button.png")
        self.footer.blit(selectButton, (280,5))
        options = self.footerFont.render("options", True, (255,255,255))
        self.footer.blit(options, (315,3))

        direction = pygame.image.load("theme/direction.png")
        self.footer.blit(direction, (4,2))
        options = self.footerFont.render("select", True, (255,255,255))
        self.footer.blit(options, (26,3))


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
        
        self.renderFooter(screen)
        self.header.render(screen)

        if(self.optionsMenu != None):
            self.optionsMenu.render(screen)
    
    def renderFooter(self, screen):
        screen.blit(self.footer, (0,self.config["screenHeight"] - self.footerHeight))
    
 
    
    def __init__(self, screen):
        print("Main Menu Init")
        self.loadSystemImages(screen)
        self.screen = screen
        self.banderole = pygame.Surface((480,80),pygame.SRCALPHA)
        self.banderole.fill((255,255,255, 160))
        self.initFooter()  
        self.header = Header.Header(24)  