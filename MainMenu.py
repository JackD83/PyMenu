import RenderObject, Configuration, SelectionMenu, FileChooser, Runner, Header, TextInput, ConfigMenu
import Footer, Keys, RenderControl, InfoOverlay, Common, NativeAppList,TaskHandler, ConfirmOverlay
import os, ResumeHandler, Suspend, IPKManager
import json, time, math, copy
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

    themeName = config["options"]["themeName"]
    

   
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
      
               
        self.loadSystem(self.currentIndex)
        self.loadSystem(self.getPrev())
        self.loadSystem(self.getNext())         

        thread = Thread(target = self.loadImagesAsync, args = ())
        thread.start()   
    
    def setOverlay(self, overlay):
        self.overlay = overlay
        RenderControl.setDirty()

    
    def loadSystem(self, index):
        if(index >= len(self.config["mainMenu"])):
            return

        entry = self.config["mainMenu"][index]
      
     
        if entry["visible"] and "icon" in entry and entry["icon"] != None and os.path.exists(entry["icon"]):
            self.systems[index] = Common.aspect_scale(Common.loadCachedImage( entry["icon"]), 140, 70)
        
        if entry["visible"] and "background" in entry and os.path.exists(entry["background"]):
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
                if event.key == Keys.DINGOO_BUTTON_START:
                    if(self.selection == "band" and "useSelection" in self.config["mainMenu"][self.currentIndex] 
                    and self.config["mainMenu"][self.currentIndex]["useSelection"] == False):          
                        self.emulatorCallback("", Keys.DINGOO_BUTTON_START, True)
                        RenderControl.setDirty()
                    else:
                        self.select()
                if event.key == Keys.DINGOO_BUTTON_A:
                   self.select()

    def select(self):
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
        if(Configuration.isRG350()):
            self.overlay = SelectionMenu.SelectionMenu(self.screen, ["Poweroff", "Reboot"], self.contextMenuCallback)
        else:
            self.overlay = SelectionMenu.SelectionMenu(self.screen, ["Poweroff", "Reboot", "Mount USB", "Start Network", "Run Gmenu2x"], self.contextMenuCallback)
    
    def openOptions(self):
        if("allowEdit" in self.config["options"] and self.config["options"]["allowEdit"]  
        and self.config["mainMenu"][self.currentIndex]["type"] == "lastPlayed"):
            self.overlay = SelectionMenu.SelectionMenu(self.screen, ["add new entry", "edit entry"], self.optionsCallback)


        elif("allowEdit" in self.config["options"] and self.config["options"]["allowEdit"]  ):
            self.overlay = SelectionMenu.SelectionMenu(self.screen, ["add new entry", "edit entry", "remove entry"], self.optionsCallback)

    def openSettings(self):
        options = json.load(open('config/options.json'))
        theme = None
        for opt in options:
            if opt["id"] == "themeName":
                theme = opt

        #append dynamic theme selection
        if(theme != None):
            theme["values"] = []
            theme["names"] = []

            itemlist = os.listdir("theme/themes")
            for item in itemlist:
                if(item.endswith(".json")):
                    theme["values"].append(item.replace(".json", ""))
                    theme["names"].append(item.replace(".json", ""))


        #filter options to show only the relevant ones
        if(Configuration.isRG350):
            options = Common.removeOptionsEntries(options, ["displayTimeout", "suspendTimeout", "volumeControl","defaultVolume"])

        if(self.config["type"] != "K3P"):
            options = Common.removeOptionsEntries(options, ["volumeControl"])


        self.subComponent = ConfigMenu.ConfigMenu(self.screen, "General Settings (PyMenu v" + str(self.config["version"]) + ")",{"textColor":(255,255,255), "backgroundColor":(0,0,0)}, \
                                        Configuration.getPathData("options"), options ,self.configCallback)
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

        if(text == "Run Gmenu2x"):
            print("Running gmenu 2x")
            Common.gmenu2x()

        if(text == "Start Network"):
            Common.startNetwork()

        if(text == "IPK Manager"):
            self.subComponent = IPKManager.IPKManager(self.screen, self.ipkCallback)
            footer = Footer.Footer([("theme/direction.png","select")], [("theme/b_button.png", "back"), ("theme/select_button.png", "options")], (255,255,255)) 
            self.subComponent.setFooter(footer)

    def ipkCallback(self, res):
        self.subComponent = None
        Configuration.reloadConfiguration()
        self.currentIndex = 0

        self.reload()

    def usbMountCallback(self, key):      
        self.overlay = None     
       

    def configCallback(self, select):

        newThemeName = self.config["options"]["themeName"]
        if(self.themeName != self.config["options"]["themeName"]):
            print("Theme changed")
            self.config["options"]["themeName"] = newThemeName     
     
        self.subComponent = None     

        Configuration.saveOptions(self.config["options"])

        self.reload()
        self.suspend.configUpdated()
        RenderControl.setDirty()

    def openSelection(self, current):
        print("Opening selection")       
        ResumeHandler.setLastUsedMain(current, self.currentIndex)

        if(current["type"] == "emulator"):            

            if("useSelection" in current and current["useSelection"] == False):
                print("Running emulator directly")
                self.emulatorCallback("", Keys.DINGOO_BUTTON_A, False)
                return


            print("Opening emulator file selection")
            options = {}
            options["entry"] = self.config["mainMenu"][self.currentIndex]
            options["textColor"] = (55,55,55)
            options["background"] = current["background"]
            options["useSidebar"] = True
            options["useGamelist"] = current["useGamelist"] if "useGamelist" in current else False
        

            if("description" in current):
                options["description"] = current["description"]

            if("folderIcon" in current):
                options["folderIcon"] = current["folderIcon"]
            
            if("previews" in current):
                options["previews"] = current["previews"]
            
            if("fileFilter" in current):
                options["fileFilter"] = current["fileFilter"]

            if("useFileFilter" in current):
                options["useFileFilter"] = current["useFileFilter"]
            
            if("limitSelection" in current):
                options["limitSelection"] = current["limitSelection"]
            
            if("hideFolders" in current):
                options["hideFolders"] = current["hideFolders"]
            
            options["selectionPath"] = current["selectionPath"]

            self.subComponent = FileChooser.FileChooser(self.screen, current["name"], current["selectionPath"], False, options, self.emulatorCallback)
            footer = Footer.Footer([("theme/direction.png","select")], [("theme/b_button.png", "back"),("theme/start_button.png", "Open with"), ("theme/a_button.png", "select")], (255,255,255)) 
            self.subComponent.setFooter(footer)
               
                     
        if(current["type"] == "native"):
            print("Opening native selection")
            options = {}
            options["background"] = current["background"]
            options["useSidebar"] = True

            if("linkPath" in current):
                options["linkPath"] = current["linkPath"]
         
            self.subComponent = NativeAppList.NativeAppList(self.screen, current["name"], current["data"] , options, self.nativeCallback)
            if("allowEdit" in self.config["options"] and self.config["options"]["allowEdit"] ):
                footer = Footer.Footer([("theme/direction.png","select")], [("theme/b_button.png", "back"), ("theme/a_button.png", "select"), ("theme/select_button.png", "options")], (255,255,255)) 
            else:
                footer = Footer.Footer([("theme/direction.png","select")], [("theme/b_button.png", "back"), ("theme/a_button.png", "select")], (255,255,255)) 
            self.subComponent.setFooter(footer)
        if(current["type"] == "lastPlayed" or current["type"] == "favourites"):
            print("Opening customList selection")
            options = {}
            options["background"] = current["background"]
            options["useSidebar"] = True
            options["type"] = current["type"]
            self.subComponent = NativeAppList.NativeAppList(self.screen, current["name"], current["data"] , options, self.customListCallback)        
            footer = Footer.Footer([("theme/direction.png","select")], [("theme/b_button.png", "back"), ("theme/a_button.png", "select")], (255,255,255)) 
            self.subComponent.setFooter(footer)  

    def nativeCallback(self, selection):
        self.subComponent = None
        if(selection != None):
            Runner.runNative(selection)

    def customListCallback(self, selection):
        self.subComponent = None
        print(json.dumps(selection, indent=2))
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
            elif(self.config["mainMenu"][self.currentIndex]["type"] == "lastPlayed"):
                conf = json.load(open('config/optionsLastPlayed.json'))
            else: 
                conf = json.load(open('config/native.json'))

            #rg350 does not support individual overclocking, remove option
            if(Configuration.isRG350()):
                for opt in conf:
                    if(opt["id"] == "overclock" ):
                        conf.remove(opt)
                        break
                     

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
            Configuration.reloadConfiguration()
            self.currentIndex = 0

            self.reload()
    
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

        #set current on the first visible
        self.currentIndex = 0
        self.currentIndex = self.getNext()
        self.currentIndex = self.getPrev()

        self.systems = [None] * len(self.config["mainMenu"])     
        self.systembackgrounds = [None] * len(self.config["mainMenu"])

        Configuration.reloadConfiguration()
        self.config = Configuration.getConfiguration()     
        self.loadSystemImages()
    
    
    def textCallback(self, text):
        print("Text callback, got text: " + text)
        self.subComponent = None

    def emulatorCallback(self, selectedFile, key=Keys.DINGOO_BUTTON_A, direct=False):
        self.selectedFile = selectedFile
       
        if("emu" in self.config["mainMenu"][self.currentIndex] and selectedFile != None):
            emus = []
            for e in self.config["mainMenu"][self.currentIndex]["emu"]:
                emus.append(e["name"])

            if(len(emus) > 0 and key == Keys.DINGOO_BUTTON_START):
                overlay = SelectionMenu.SelectionMenu(self.screen, emus, self.emuSelectionCallback)
                if(direct):
                    self.overlay = overlay
                else:
                    self.subComponent.setOverlay(overlay)

            elif(len(emus) > 0):
                 self.emuSelectionCallback(0, emus[0])
        
            elif(len(emus) == 0):
                self.subComponent = None
                self.overlay = ConfirmOverlay.ConfirmOverlay("Emu not configured!", (255,255,255),  [("theme/a_button.png", "OK")],self.clearOverlay)
                RenderControl.setDirty()

            return

        ##old config
        self.subComponent = None
        if(selectedFile != None):
                Runner.runEmu(self.config["mainMenu"][self.currentIndex], selectedFile)
     
  
    def emuSelectionCallback(self, index, selection):
       
        if(self.subComponent != None):
            self.subComponent.setOverlay(None)
        else:
            self.overlay = None

        if(index != -1):
            self.subComponent = None

            if(self.selectedFile != None):
                data = copy.deepcopy(self.config["mainMenu"][self.currentIndex])
                data["cmd"] = data["emu"][index]["cmd"]
                data["workingDir"] = data["emu"][index]["workingDir"]
                if "params" in data["emu"][index]: data["params"] = data["emu"][index]["params"]
                Runner.runEmu(data, self.selectedFile)
     
            print(str(selection) + " " + str(index) + " " + str(data["emu"][index]))

    def infoCallback(self, res):
        self.overlay = None
        
        self.config["firstStart"] = False
        Configuration.saveConfiguration()
    
    
    def getNext(self, stride=1): 

      
       
        if(self.currentIndex + stride >= len(self.systems)):
            index = (self.currentIndex + stride) - len(self.systems)                   
        else:
            index = self.currentIndex + stride
     
        if(self.config["mainMenu"][index]["visible"] ):           
            return index
        else:
            return self.getNext(stride + 1) 

    def getPrev(self, stride=1):    
       
        if(self.currentIndex - stride < 0):
            index =  len(self.systems) - int(math.fabs(self.currentIndex - stride))
        else:
            index = self.currentIndex - stride      

        if(self.config["mainMenu"][index]["visible"] ):          
            return index
        else:         
            return self.getPrev(stride + 1)


        
    def clearOverlay(self, res):
        self.overlay = None

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
        if(self.inTransition and self.transitionOffset != 0 and not Configuration.isRS97() and not Configuration.isRG350()):
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

  

    
    def __init__(self, screen, suspend):
        print("Main Menu Init")
        self.screen = screen
        self.suspend = suspend
        self.banderole = pygame.Surface((self.config["screenWidth"],80),pygame.SRCALPHA)

        Runner.setMainMenu(self)

        self.systems = [None] * len(self.config["mainMenu"])     
        self.systembackgrounds = [None] * len(self.config["mainMenu"])
        self.currentIndex = self.getNext()
        self.currentIndex = self.getPrev()
   
      
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