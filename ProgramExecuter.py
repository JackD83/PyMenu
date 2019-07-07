import RenderObject, Configuration, NativeAppList, ConfigMenu, Footer, ConfirmOverlay
import os, Keys, RenderControl, Common, SelectionMenu, FileChooser
import pygame, sys, ResumeHandler, os, subprocess
import platform
import json
from operator import itemgetter
from threading import Thread

class ProgramExecuter(NativeAppList.NativeAppList):

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

                    self.callback()
                    RenderControl.setDirty()


    def runCMD(self, cmd):
        self.proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

        thread = Thread(target = self.updateList, args = ())
        thread.start()

        

    def updateList(self):
        while self.proc.poll() is None:
            output = self.proc.stdout.readline()
            self.data.append({
                "name": output
            })
            self.initList()
            self.setSelection(0)

        print("programm terminated")

        self.data.append({
                "name": "Programm terminated, press b to go back"
            })
        self.initList()
        self.setSelection(0)
        RenderControl.setDirty()
    


    def __init__(self, screen, title, cmd, callback):        
        data = []
        options = {}
        self.cmd = cmd

        NativeAppList.NativeAppList.__init__(self, screen, title, data, options, callback)

        self.runCMD(cmd)
       