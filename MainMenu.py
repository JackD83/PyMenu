import RenderObject, Configuration, SelectionMenu, FileChooser, Runner, Header, TextInput, ConfigMenu
import Footer, Keys, RenderControl, InfoOverlay, Common, NativeAppList,TaskHandler, ConfirmOverlay
import os
import json
import pygame, sys, subprocess,platform
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
    systemIconOffet = (480 - config["screenWidth"]) / 2
   
    overlay = None
    subComponent = None
        
    def loadSystemImages(self):
        self.systems = []
        self.systemNames = []
        self.systembackgrounds = []

        for entry in self.config["mainMenu"]:
            try:
                self.systems.append(Common.aspect_scale(Common.loadCachedImage( entry["icon"]), 140, 70))
                self.systembackgrounds.append( pygame.transform.scale(Common.loadCachedImage( entry["background"]), ( self.config["screenWidth"],self.config["screenHeight"]) ))
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
                    self.openContextMenu()
                    RenderControl.setDirty()
                if event.key == Keys.DINGOO_BUTTON_VOL_DOWN or event.key == Keys.DINGOO_BUTTON_VOL_UP:
                    self.header.updateVolume()
                    RenderControl.setDirty()

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
        self.overlay = SelectionMenu.SelectionMenu(self.screen, ["add new entry", "edit entry", "remove entry"], self.optionsCallback)

    def openContextMenu(self):
        self.overlay = SelectionMenu.SelectionMenu(self.screen, ["Mount USB", "Poweroff", "Reboot", "Options"], self.contextMenuCallback)

    def contextMenuCallback(self, selection):
        self.overlay = None
      
        if(selection == 0):          
            print("Mounting USB")
            options = {}
            options["cmd"] = "/opt/usb/usb.sh"
            Runner.runNative(options)
           
        if(selection == 1):
            if(platform.processor() == ""):
                subprocess.Popen(["poweroff"])
            else:
                print("Poweroff")
             
        if(selection == 2):
            if(platform.processor() == ""):
                subprocess.Popen(["reboot"])
            else:
                print("reboot")
        if(selection == 3):          
            self.subComponent = ConfigMenu.ConfigMenu(self.screen, "General Options",{"textColor":(255,255,255), "backgroundColor":(0,0,0)}, \
                                        Configuration.getPathData("options"), json.load(open('config/options.json')) ,self.configCallback)
            footer = Footer.Footer([("theme/direction.png","select")], [("theme/b_button.png", "back"), ("theme/a_button.png", "change"), ("theme/start_button.png", "save")], (255,255,255)) 
            self.subComponent.setFooter(footer)
            RenderControl.setDirty()

    def configCallback(self, select):
        self.subComponent = None
        RenderControl.setDirty()

    def openSelection(self):
        print("Opening selection")
        current = self.config["mainMenu"][self.currentIndex]

        if(current["type"] == "emulator"):
            print("Opening emulator file selection")
            options = {}
            options["textColor"] = (55,55,55)
            options["background"] = current["background"]
            options["useSidebar"] = True

            if("description" in current):
                options["description"] = current["description"]

            if("folderIcon" in current):
                options["folderIcon"] = current["folderIcon"]
            
            if("previews" in current):
                options["previews"] = current["previews"]
            
            if("fileFilter" in current):
                options["fileFilter"] = current["fileFilter"]

            self.subComponent = FileChooser.FileChooser(self.screen, current["name"], current["selectionPath"], False, options, self.emulatorCallback)
            footer = Footer.Footer([("theme/direction.png","select")], [("theme/b_button.png", "back"), ("theme/a_button.png", "select")], (255,255,255)) 
            self.subComponent.setFooter(footer)
               
                     
        if(current["type"] == "native"):
            print("Opening native selection")
            options = {}
            options["background"] = current["background"]
            options["useSidebar"] = True
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
        if(optionID == 0):
            self.overlay = SelectionMenu.SelectionMenu(self.screen, ["Emulator", "Native"], self.typeAddCallback)
        if(optionID == 1):
            conf = None
            if(self.config["mainMenu"][self.currentIndex]["type"] == "emulator"):              
                conf = json.load(open('config/entry.json'))
            else:               
                conf = json.load(open('config/native.json'))

            self.subComponent = ConfigMenu.ConfigMenu(self.screen, "Edit menu entry",{"textColor":(55,55,55), "backgroundColor":(221,221,221)}, \
                                        self.config["mainMenu"][self.currentIndex] ,conf ,self.addEditCallback)
            footer = Footer.Footer([("theme/direction.png","select")], [("theme/b_button.png", "back"), ("theme/a_button.png", "change"), ("theme/start_button.png", "save")], (255,255,255)) 
            self.subComponent.setFooter(footer)
        if(optionID == 2):
            self.overlay = ConfirmOverlay.ConfirmOverlay("really delete?", (255,255,255),  [("theme/b_button.png", "back"), ("theme/a_button.png", "delete")], self.deleteCallback)
            RenderControl.setDirty()


    def typeAddCallback(self, t):
        self.overlay = None

        data = None
        conf = None
        if(t==0):
            data = self.getEmptyEmulatorData()
            conf = json.load(open('config/entry.json'))
        else:
            data = self.getEmptyNativeData()
            conf = json.load(open('config/native.json'))

        self.subComponent = ConfigMenu.ConfigMenu(self.screen, "Add new menu entry",{"textColor":(255,255,255), "backgroundColor":(0,0,0)}, \
                                   data ,conf ,self.addEditCallback)
        footer = Footer.Footer([("theme/direction.png","select")], [("theme/b_button.png", "back"), ("theme/a_button.png", "change"), ("theme/start_button.png", "save")], (255,255,255)) 
        self.subComponent.setFooter(footer)
       

    def deleteCallback(self, res):
        self.overlay = None
        if(res == 1 and len(self.config["mainMenu"])  > 1):
            del self.config["mainMenu"][self.currentIndex]
            Configuration.saveConfiguration()
            self.currentIndex = 0
            self.loadSystemImages()
    
    def getEmptyEmulatorData(self):
        emptyEntry = {
            "name": "Emulator",
            "type": "emulator",            
            "background": "backgrounds",
            "icon": "systems",
            "cmd": ".",
            "workingDir": None,           
            "selectionPath": ".",
            "previews": None,
            "legacy":False,
            "screen":"default",
            "overclock":"524"
        }
        return emptyEntry

    def getEmptyNativeData(self):
        emptyEntry = {
            "name": "Native",
            "type": "native",            
            "background": "backgrounds",
            "icon": "systems",
            "data": []               
        }
        return emptyEntry

    def addEditCallback(self, entry):
        self.subComponent = None

        print(entry)

        if(entry == None):
            self.reload()
            return

        if(entry["background"] == None or not os.path.isfile(entry["background"])):
            print("Background does not exist! ")
            self.reload()
            return

        if(entry["icon"] == None or not os.path.isfile(entry["icon"])):
            print("Icon does not exist! ")
            self.reload()
            return
      
      
        if(entry != None and not entry in self.config["mainMenu"]):
           self.config["mainMenu"].insert(self.currentIndex, entry)

        Configuration.saveConfiguration()
        self.loadSystemImages()
        RenderControl.setDirty()       
    
    def reload(self):
        Configuration.reloadConfiguration()
        self.config = Configuration.getConfiguration()
        self.loadSystemImages()
    
    
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
        screen.blit(self.systems[self.currentIndex], ( (self.config["screenWidth"] / 2 - self.systems[self.currentIndex].get_width() / 2) + self.transitionOffset , 40 + 80  -self.systems[self.currentIndex].get_height() / 2 ))

        #previous
        screen.blit(self.systems[self.getPrev()], (0  + self.transitionOffset  - self.systemIconOffet, 40 + 80  -self.systems[self.getPrev()].get_height() / 2 ))

        #next
        screen.blit(self.systems[self.getNext()], ( (self.config["screenWidth"] - self.systems[self.currentIndex].get_width())  + self.transitionOffset + self.systemIconOffet, 40 + 80  -self.systems[self.getNext()].get_height() / 2 ))
        
        if(self.footer != None):
            self.footer.render(screen)

        self.header.render(screen)

        if(self.overlay != None):
            self.overlay.render(screen)           
   
 
    
    def __init__(self, screen):
        print("Main Menu Init")
        self.loadSystemImages()
        self.screen = screen
        self.banderole = pygame.Surface((self.config["screenWidth"],80),pygame.SRCALPHA)
        self.banderole.fill((255,255,255, 160))
      
        self.header = Header.Header(24)

        if("firstStart" in self.config and self.config["firstStart"]):
             self.overlay = InfoOverlay.InfoOverlay("theme/info.png", self.infoCallback)

        #self.footer = Footer.Footer([("theme/direction.png","select")], [("theme/select_button.png", "options"), ("theme/a_button.png", "open")], (255,255,255))