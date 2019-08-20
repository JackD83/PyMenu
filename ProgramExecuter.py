import RenderObject, Configuration, NativeAppList, ConfigMenu, Footer, ConfirmOverlay
import os, Keys, RenderControl, Common, SelectionMenu, FileChooser
import pygame, sys, ResumeHandler, os, subprocess, TaskHandler
import platform
import json
from operator import itemgetter
from threading import Thread

class ProgramExecuter(NativeAppList.NativeAppList):

    isTerminated = False

    def handleEvents(self, events):
        if(self.subComponent != None):
            self.subComponent.handleEvents(events)          
            return


        if(self.overlay != None):
            self.overlay.handleEvents(events)            
            return

         
        for event in events:    
            if event.type == pygame.KEYDOWN:
                self.keyDown = True
                if(self.isTerminated):
                    if event.key == Keys.DINGOO_BUTTON_UP:
                        if(not len(self.entryList) <= 1):
                            self.up()
                            self.onChange()
                            RenderControl.setDirty()
                    if event.key == Keys.DINGOO_BUTTON_DOWN:
                        if(not len(self.entryList) <= 1):   
                            self.down()
                            self.onChange()
                            RenderControl.setDirty()
                    if event.key == Keys.DINGOO_BUTTON_L:
                        self.up(self.maxListEntries)
                        self.onChange()
                        RenderControl.setDirty()
                    if event.key == Keys.DINGOO_BUTTON_R:
                        self.down(self.maxListEntries)
                        self.onChange()
                        RenderControl.setDirty()
                
                    if event.key == Keys.DINGOO_BUTTON_B:
                            self.callback()
                            RenderControl.setDirty()
         
           


    def runCMD(self, cmd):
        os.environ['PYTHONUNBUFFERED'] = "1"
        self.proc = subprocess.Popen(cmd, shell=True, bufsize=1, stdout=subprocess.PIPE,stderr = subprocess.STDOUT,universal_newlines = True)

        thread = Thread(target = self.updateList, args = ())
        thread.start()
        RenderControl.setDirty()

        self.updateTask = TaskHandler.addPeriodicTask(100,  RenderControl.setDirty , delay=0)



    def updateList(self):
        while self.proc.poll() is None:
            output = self.proc.stdout.readline()
            if(output != ""):
                print("stout: " + output.rstrip())
                self.data.append({
                    "name": output.rstrip()
                })

            # output = self.proc.stderr.readline()
            # if(output != ""):
            #     print("sterr: " + output.rstrip())
            #     self.data.append({
            #         "name": output.rstrip()
            #     })

            self.initList()
            self.setSelection(len(self.data) - 1)
         
            RenderControl.setDirty()
       
        self.data.append({
                 "name": ""
             })

        self.data.append({
                 "name": "Task finished, press 'B' to go back"
             })

        self.initList()
        self.setSelection(len(self.data) - 1)
    
        RenderControl.setDirty()
      
        self.isTerminated = True
        TaskHandler.removePeriodicTask(self.updateTask)
    


    def __init__(self, screen, title, cmd, callback):        
        data = []
        options = {}
        self.cmd = cmd
        self.wrapArround = False


        NativeAppList.NativeAppList.__init__(self, screen, title, data, options, callback)

        self.runCMD(cmd)
       