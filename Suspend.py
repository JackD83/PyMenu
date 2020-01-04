import pygame, sys, Common, TaskHandler, Configuration
import os,subprocess


class Suspend():

    
    suspendTaskId = None

    brightnessTaskId = None
    config = Configuration.getConfiguration()

    displayDark = False

    def handleEvents(self, events):
        if(len(events) > 0):
            self.addSuspendTask()
            self.restoreScreen()
            self.addBrignessTask()
    
    def configUpdated(self):
        self.addSuspendTask()
        self.addBrignessTask()

    def suspend(self):
        try:
            subprocess.Popen(["poweroff"])
            TaskHandler.removePeriodicTask(self.suspendTaskId)
        except Exception as identifier:
            pass
      

    def disableScreen(self):   
        if(Configuration.isRG350()):
            return

        os.system('echo 0 > /proc/jz/backlight')
        self.displayDark = True
        TaskHandler.removePeriodicTask(self.brightnessTaskId)

    def restoreScreen(self):
        if(Configuration.isRG350()):
            return

        if(self.displayDark):
            if("lcd_backlight" not in self.config):
                self.config["lcd_backlight"] = 30
                Configuration.saveConfiguration()

            backlight = self.config["lcd_backlight"] 
            
            os.system('echo ' + str(backlight) + ' > /proc/jz/backlight')
            self.displayDark = False

    def disableSuspend(self):
        if(self.suspendTaskId is not None):
            TaskHandler.removePeriodicTask(self.suspendTaskId)

    def addSuspendTask(self):
        if(self.suspendTaskId is not None):
            TaskHandler.removePeriodicTask(self.suspendTaskId)
        suspendTime = self.config["options"]["suspendTimeout"]
        if(suspendTime == "off"):
            return

        self.suspendTaskId = TaskHandler.addPeriodicTask(0, self.suspend,  float(suspendTime) * 1000 * 60)
    
    def addBrignessTask(self):
        if(self.brightnessTaskId is not None):
            TaskHandler.removePeriodicTask(self.brightnessTaskId)
        displayTimeout = self.config["options"]["displayTimeout"]
        if(displayTimeout == "off"):
            return


        self.brightnessTaskId = TaskHandler.addPeriodicTask(0, self.disableScreen,  float(displayTimeout) * 1000)

    
           


    def __init__(self):
        Configuration.addConfigChangedCallback(self.configUpdated)
        self.addSuspendTask()
        self.addBrignessTask()
       


