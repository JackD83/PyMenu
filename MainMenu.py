import RenderObject, Configuration, SelectionMenu, FileChooser, Runner, Header, TextInput, ConfigMenu
import Footer, Keys, RenderControl, InfoOverlay, Common, NativeAppList,TaskHandler, ConfirmOverlay
import os, ResumeHandler, Suspend
import json, time, math
import pygame, sys, subprocess,platform
from pprint import pprint
from threading import Thread

class MainMenu(RenderObject.RenderObject):
    config = Configuration.getConfiguration()
    theme = Configuration.getTheme()
   
    gear = Common.aspect_scale(Common.loadCachedImage("theme/gear.png"),20,20)
    gearFinal = None

    power = Common.aspect_scale(Common.loadCachedImage("theme/power.png"),18,18)
    powerFinal = None   

   
    header = None
    footer = None
    systems = []

    systembackgrounds = []
    currentIndex = 0
    inTransition = False
    transitionOffset = 0
    systemOffset = 160
    systemIconOffet = (480 - config["screenWidth"]) / 2
   
    overlay = None
    subComponent = None

    selection = "band"
        
    def loadSystemImages(self):
      
        self.systems = [None] * len(self.config["mainMenu"])
     
        self.systembackgrounds = [None] * len(self.config["mainMenu"])

        self.loadSystem(self.currentIndex)
        self.loadSystem(self.getPrev())
        self.loadSystem(self.getNext())         

        thread = Thread(target = self.loadImagesAsync, args = ())
        thread.start()   

    
    def loadSystem(self, index):
        if(index >= len(self.config["mainMenu"])):
            return

        entry = self.config["mainMenu"][index]
        self.systems[index] = Common.aspect_scale(Common.loadCachedImage( entry["icon"]), 140, 70)
        self.systembackgrounds[index] = pygame.transform.scale(Common.loadCachedImage( entry["background"]), ( self.config["screenWidth"],self.config["screenHeight"]) )
     

    def loadImagesAsync(self):
        for index, systemImage in enumerate(self.systems):
            try:
                if(systemImage is None):
                    self.loadSystem(index) 
            except ValueError:
                pass

        print("processed ", len(self.systems), " entries")       
    
    def handleEvents(self, events):   
        if(self.subComponent != None):
            self.subComponent.handleEvents(events)
            return

        if(self.overlay != None):
            self.overlay.handleEvents(events)
            return

        for event in events:    
            if event.type == pygame.KEYDOWN:      
                if event.key == Keys.DINGOO_BUTTON_DOWN:
                    if(self.selection == "band"):
                        self.selection = "power"
                        RenderControl.setDirty()
                if event.key == Keys.DINGOO_BUTTON_UP:
                    if(self.selection == "power" or self.selection == "settings"):
                        self.selection = "band"
                        RenderControl.setDirty()
                if event.key == Keys.DINGOO_BUTTON_LEFT or event.key == Keys.DINGOO_BUTTON_L:
                    if(not self.inTransition and self.selection == "band"):
                        TaskHandler.addAnimation(0, 160, 200, self.transitionCallback)
                        self.inTransition = True             
                        
                    if( self.selection == "power"):
                        self.selection = "settings"

                    RenderControl.setDirty()
                if event.key == Keys.DINGOO_BUTTON_RIGHT or event.key == Keys.DINGOO_BUTTON_R:
                    if(not self.inTransition and self.selection == "band"):
                        TaskHandler.addAnimation(0, -160,200, self.transitionCallback)
                        self.inTransition = True             
                       
                    if( self.selection == "settings"):
                        self.selection = "power"
                    
                    RenderControl.setDirty()
                if event.key == Keys.DINGOO_BUTTON_SELECT:                    
                    self.openOptions()
                    RenderControl.setDirty()
                if event.key == Keys.DINGOO_BUTTON_A:
                    if(self.selection == "band"):
                        self.openSelection(self.config["mainMenu"][self.currentIndex])
                    if(self.selection == "power"):
                       self.openPowerMenu()
                    
                    if(self.selection == "settings"):
                        self.openSettings()

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

    def openPowerMenu(self):
        self.overlay = SelectionMenu.SelectionMenu(self.screen, ["Poweroff", "Reboot", "Mount USB"], self.contextMenuCallback)
    
    def openOptions(self):
        if("allowEdit" in self.config["options"] and self.config["options"]["allowEdit"] ):
            self.overlay = SelectionMenu.SelectionMenu(self.screen, ["add new entry", "edit entry", "remove entry"], self.optionsCallback)

    def openSettings(self):
        self.subComponent = ConfigMenu.ConfigMenu(self.screen, "General Settings",{"textColor":(255,255,255), "backgroundColor":(0,0,0)}, \
                                        Configuration.getPathData("options"), json.load(open('config/options.json')) ,self.configCallback)
        footer = Footer.Footer([("theme/direction.png","select")], [("theme/b_button.png", "back"), ("theme/a_button.png", "change"), ("theme/start_button.png", "save")], (255,255,255)) 
        self.subComponent.setFooter(footer)
        RenderControl.setDirty()   

    def contextMenuCallback(self, selection, text):
        self.overlay = None
      
        if(text == "Mount USB"):          
            print("Mounting USB")
            Common.mountUSB()
            self.suspend.disableSuspend()
            self.overlay = InfoOverlay.InfoOverlay("theme/usb.png", self.usbMountCallback)
           
        if(text == "Poweroff"):
            if(platform.processor() == ""):
                subprocess.Popen(["sync"])
                subprocess.Popen(["poweroff"])
            else:
                print("Poweroff")
             
        if(text == "Reboot"):
            if(platform.processor() == ""):
                subprocess.Popen(["sync"])
                subprocess.Popen(["reboot"])
            else:
                print("reboot")

    def usbMountCallback(self, key):
        print("Rebooting after usb mount")
        if(platform.processor() == ""):
            subprocess.Popen(["sync"])
            subprocess.Popen(["reboot"])
        else:
            print("reboot")
            self.overlay = None
       

    def configCallback(self, select):
        self.subComponent = None
        isLastPlayed = self.config["mainMenu"][self.currentIndex]["type"] == "lastPlayed" 
        Configuration.saveConfiguration()
        if(isLastPlayed and "showLastPlayed" in self.config["options"] and not self.config["options"]["showLastPlayed"]):
            self.currentIndex = 0

        self.reload()
        RenderControl.setDirty()

    def openSelection(self, current):
        print("Opening selection")       
        ResumeHandler.setLastUsedMain(current, self.currentIndex)

        if(current["type"] == "emulator"):            

            if("useSelection" in current and current["useSelection"] == False):
                print("Running emulator directly")
                Runner.runNative(self.config["mainMenu"][self.currentIndex])
                return


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
            if("allowEdit" in self.config["options"] and self.config["options"]["allowEdit"] ):
                footer = Footer.Footer([("theme/direction.png","select")], [("theme/b_button.png", "back"), ("theme/a_button.png", "select"), ("theme/select_button.png", "options")], (255,255,255)) 
            else:
                footer = Footer.Footer([("theme/direction.png","select")], [("theme/b_button.png", "back"), ("theme/a_button.png", "select")], (255,255,255)) 
            self.subComponent.setFooter(footer)
        if(current["type"] == "lastPlayed"):
            print("Opening native selection")
            options = {}
            options["background"] = current["background"]
            options["useSidebar"] = True
            options["type"] = "lastPlayed"
            self.subComponent = NativeAppList.NativeAppList(self.screen, current["name"], current["data"] , options, self.lastPlayedCallback)        
            footer = Footer.Footer([("theme/direction.png","select")], [("theme/b_button.png", "back"), ("theme/a_button.png", "select")], (255,255,255)) 
            self.subComponent.setFooter(footer)  

    def nativeCallback(self, selection):
        self.subComponent = None
        if(selection != None):
            Runner.runNative(selection)

    def lastPlayedCallback(self, selection):
        self.subComponent = None
        if(selection != None):
            if(selection["type"] == "native"):
                Runner.runNative(selection)
            elif(selection["type"] == "emulator"):
                Runner.runEmu(selection, selection["rom"])
    


    def optionsCallback(self, optionID, text):
        print("Options came back with: ", optionID)
        self.overlay = None
        if(optionID == 0):
            self.overlay = SelectionMenu.SelectionMenu(self.screen, ["Emulator", "Native"], self.typeAddCallback)
        if(optionID == 1):
            conf = None
            if(self.config["mainMenu"][self.currentIndex]["type"] == "emulator"):              
                conf = json.load(open('config/entry.json'))
                if(not Configuration.isRS97()):                  
                    conf = conf + json.load(open('config/pap.json'))
            else:               
                conf = json.load(open('config/native.json'))

            self.subComponent = ConfigMenu.ConfigMenu(self.screen, "Edit menu entry",{"textColor":(55,55,55), "backgroundColor":(221,221,221)}, \
                                        self.config["mainMenu"][self.currentIndex] ,conf ,self.addEditCallback)
            footer = Footer.Footer([("theme/direction.png","select")], [("theme/b_button.png", "back"), ("theme/a_button.png", "change"), ("theme/start_button.png", "save")], (255,255,255)) 
            self.subComponent.setFooter(footer)
        if(optionID == 2):
            self.overlay = ConfirmOverlay.ConfirmOverlay("really delete?", (255,255,255),  [("theme/b_button.png", "back"), ("theme/a_button.png", "delete")], self.deleteCallback)
            RenderControl.setDirty()


    def typeAddCallback(self, t, text):
        self.overlay = None

        data = None
        conf = None
        if(t==0):
            data = self.getEmptyEmulatorData()
            conf = json.load(open('config/entry.json'))
            if(not Configuration.isRS97()):
                conf = conf + json.load(open('config/pap.json'))
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
             "useSelection" : True,         
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
        self.loadLastPlayed()
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
    
    
    def getNext(self, stride=1):     
        if(self.currentIndex + stride >= len(self.systems)):
            return (self.currentIndex + stride) - len(self.systems)
        else:
            return self.currentIndex + stride

    def getPrev(self, stride=1):       
        if(self.currentIndex - stride < 0):
            return len(self.systems) - int(math.fabs(self.currentIndex - stride))
        else:
            return self.currentIndex - stride
        

    def render(self, screen):
        if(self.subComponent != None):
            self.subComponent.render(screen)
            return     
        if(self.systembackgrounds[self.currentIndex] is not None):
            screen.blit(self.systembackgrounds[self.currentIndex], (0, 0))
        else:
            RenderControl.setDirty()

        if(self.selection=="band"):
            self.banderole.fill((255,255,255, 160))
        else:
            self.banderole.fill((255,255,255, 90))

        screen.blit(self.banderole, (0,80))

        #current
        if(self.systems[self.currentIndex] is not None):
            screen.blit(self.systems[self.currentIndex], ( (self.config["screenWidth"] / 2 - self.systems[self.currentIndex].get_width() / 2) + self.transitionOffset , 40 + 80  -self.systems[self.currentIndex].get_height() / 2 ))
        else:            
            RenderControl.setDirty()

        #previous
        if(self.systems[self.getPrev()] is not None and self.systems[self.getPrev()] is not None):
            screen.blit(self.systems[self.getPrev()], (0  + self.transitionOffset  - self.systemIconOffet, 40 + 80  -self.systems[self.getPrev()].get_height() / 2 ))
        else:            
            RenderControl.setDirty()

        #next
        if(self.systems[self.getNext()] is not None and self.systems[self.currentIndex] is not None):
            screen.blit(self.systems[self.getNext()], ( (self.config["screenWidth"] - self.systems[self.currentIndex].get_width())  + self.transitionOffset + self.systemIconOffet, 40 + 80  -self.systems[self.getNext()].get_height() / 2 ))
        else:            
            RenderControl.setDirty() 

        #transition next
        if(self.inTransition and self.transitionOffset != 0 and not Configuration.isRS97()):
            index = 0  
            offset = 0
            if(self.transitionOffset > 0):
                index = self.getPrev(2)
                offset = -self.systemOffset

            elif(self.transitionOffset < 0):
                index = self.getNext(2)   
                offset = self.config["screenWidth"] - self.systems[self.currentIndex].get_width() + self.systemOffset

            if(self.systems[index] is not None and self.systems[index] is not None):
                screen.blit(self.systems[index], (offset + self.transitionOffset + self.systemIconOffet, 40 + 80  -self.systems[index].get_height() / 2 ))
            else:            
                RenderControl.setDirty()

        

        if(self.footer != None):
            self.footer.render(screen)

        self.header.render(screen)

        self.renderIcons(screen)

       
        if(self.overlay != None):
            self.overlay.render(screen)           
   
    def renderIcons(self, screen):
        powerYPos = self.config["screenHeight"] - 30
        powerXPos = self.config["screenWidth"] - 50

        if(self.powerFinal == None):
            self.powerFinal = self.power.convert_alpha().copy()
            self.powerFinal.fill((255, 255, 255, 120), None, pygame.BLEND_RGBA_MULT)  
               
        if(self.selection == "power"):
            screen.blit(self.power, (powerXPos,powerYPos))
        else:
            screen.blit(self.powerFinal, (powerXPos,powerYPos))

        settingsYPos = self.config["screenHeight"] - 30
        settingsXPos = 30     

        if(self.gearFinal == None):
            self.gearFinal = self.gear.convert_alpha().copy()
            self.gearFinal.fill((255, 255, 255, 120), None, pygame.BLEND_RGBA_MULT)  
        
        if(self.selection == "settings"):
            screen.blit(self.gear, (settingsXPos,settingsYPos))
        else:
            screen.blit(self.gearFinal, (settingsXPos,settingsYPos))

    def loadLastPlayed(self):     
        if("showLastPlayed" in self.config["options"] and self.config["options"]["showLastPlayed"] ):
            print("loading last played games")
            try:
                lastPlayed = json.load(open("config/lastPlayed.json"))
                if(not "data" in lastPlayed):
                    lastPlayed["data"] = []
                self.config["mainMenu"].append(lastPlayed)        
            except Exception as ex:
                print("Exception: " + str(ex))

    
    def __init__(self, screen, suspend):
        print("Main Menu Init")
        self.screen = screen
        self.suspend = suspend
        self.banderole = pygame.Surface((self.config["screenWidth"],80),pygame.SRCALPHA)

        self.loadLastPlayed()
        
      
        self.header = Header.Header(24)

        res = ResumeHandler.getResumeFile()
        if(res != None and res["mainIndex"] != None and res["main"] != None):
            self.currentIndex = res["mainIndex"]            

            if("useSelection" in self.config["mainMenu"][self.currentIndex] and self.config["mainMenu"][self.currentIndex]["useSelection"] != None):
                if(self.config["mainMenu"][self.currentIndex]["useSelection"] == True):
                    self.openSelection(self.config["mainMenu"][self.currentIndex])
                else:
                    ResumeHandler.clearResume()

            else:
                self.openSelection(self.config["mainMenu"][self.currentIndex])
            
        else:
            if("firstStart" in self.config and self.config["firstStart"]):
                self.overlay = InfoOverlay.InfoOverlay("theme/info.png", self.infoCallback)

        self.loadSystemImages()


        


       

        #self.footer = Footer.Footer([("theme/direction.png","select")], [("theme/select_button.png", "options"), ("theme/a_button.png", "open")], (255,255,255))