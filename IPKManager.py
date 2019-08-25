import RenderObject, Configuration, NativeAppList, ConfigMenu, Footer, ConfirmOverlay
import os, Keys, RenderControl, Common, SelectionMenu, FileChooser
import pygame, sys, ResumeHandler, os, subprocess, ProgramExecuter
import platform
import json
from operator import itemgetter

class IPKManager(NativeAppList.NativeAppList):


    def loadPackages(self):
        data = []

        try:
            out = subprocess.check_output(["opkg" , "list-installed"], shell=False)
            #out = subprocess.check_output(["dir"], shell=True)
            for line in out.splitlines():
                if(not line.lower().startswith("pymenu")):
                    data.append(
                        {
                        "name": line
                        }
                    )

        except Exception as e:
            pass

        return data

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
           
                    if(len(self.data) == 0):
                        self.overlay = SelectionMenu.SelectionMenu(self.screen, ["install new"], self.optionsCallback)
                    else:
                        self.overlay = SelectionMenu.SelectionMenu(self.screen, ["install new", "uninstall"], self.optionsCallback)
                    
                    RenderControl.setDirty()

        if(self.overlay is None):
            NativeAppList.NativeAppList.handleEvents(self, events)

    
    def optionsCallback(self, index, selection):
        self.overlay = None
        RenderControl.setDirty()

        if(selection == "install new"):
            self.installIPK()
        elif(selection == "uninstall"):
            selName = self.entryList[self.currentIndex]["name"]
            name = selName.split(" - ")[0]
            self.cmd = [ "opkg","remove", name]

            self.overlay = ConfirmOverlay.ConfirmOverlay("really uninstall?", (255,255,255),  [("theme/b_button.png", "back"), ("theme/a_button.png", "delete")], self.uninstallCallback)
            RenderControl.setDirty()


    def uninstallCallback(self, res):
        self.overlay = None
        if(res == 1):
            self.subComponent = ProgramExecuter.ProgramExecuter(self.screen, "Uninstalling IPK", self.cmd, self.executerCallback)
            self.subComponent.setFooter(None)

    def installIPK(self):
        
        print("Opening ipk file selection")
        options = {}
        options["textColor"] = (55,55,55)
       
        options["useSidebar"] = False
        options["useGamelist"] = False
        options["fileFilter"] = [".ipk", ".IPK"]
        options["useFileFilter"] = True
        options["limitSelection"] = False
        options["hideFolders"] = False
        options["selectionPath"] = "/home/retrofw"

        self.subComponent = FileChooser.FileChooser(self.screen, "IPK Selection", "/home/retrofw", False, options, self.installIPKCallback)
        footer = Footer.Footer([("theme/direction.png","select")], [("theme/b_button.png", "back"), ("theme/a_button.png", "select")], (255,255,255)) 
        self.subComponent.setFooter(footer)
        RenderControl.setDirty()

    
    def installIPKCallback(self, selection, key=Keys.DINGOO_BUTTON_A, direct=False):
        print(selection)
        if( selection.lower().find("pymenu-") != -1):
            self.subComponent = None
            self.overlay = ConfirmOverlay.ConfirmOverlay("Install with Gmenu", (255,255,255),  [("theme/b_button.png", "back")], self.pyMenuSelectedCallback)

            RenderControl.setDirty()
            return

        if(selection != None):
            #cmd = "opkg install " + selection
            cmd = [ "opkg","install", selection ,"--force-reinstall"]
            #cmd = [ "ping","localhost"]

            self.subComponent = ProgramExecuter.ProgramExecuter(self.screen, "Installing IPK", cmd, self.executerCallback)
            self.subComponent.setFooter(None)

        else:
            self.subComponent = None

    def pyMenuSelectedCallback(self, selcted):
        self.overlay = None

    def executerCallback(self):
        self.subComponent = None
        self.data = self.loadPackages()
        self.initList()
        self.onChange()


    def __init__(self, screen, callback):        
        data = self.loadPackages()
        options = {}

        NativeAppList.NativeAppList.__init__(self, screen, "IPK Manager", data, options, callback)
       