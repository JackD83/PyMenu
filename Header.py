import RenderObject, Configuration, SelectionMenu, FileChooser, Runner, TaskHandler
import os, Common, RenderControl
import pygame, sys

class Header():
    config = Configuration.getConfiguration()
    theme = Configuration.getTheme()
    headerHeight = 24
    lastVolChange = 0
    vol = 0
    volAlpha = 255
    speaker = Common.loadCachedImage("theme/speaker.png")


    battery = None
    volumeDevice = None
    volAnim = None

    batteryLevel = 0
  

    def render(self, screen):
        screen.blit(self.header, (0,0))

    def updateHeader(self):
        self.header = pygame.Surface((self.config["screenWidth"], self.headerHeight),pygame.SRCALPHA)
        self.header.fill(Configuration.toColor(self.theme["header"]["color"]))

        if(self.volAlpha > 0):
            speaker = self.speaker.convert_alpha().copy()
            speaker.fill((255, 255, 255, self.volAlpha), None, pygame.BLEND_RGBA_MULT) 
            self.header.blit(speaker, (10, (self.headerHeight - speaker.get_height()) / 2))

            vol = Common.loadCachedImage(self.getCurrentVolumeImage())
            vol = vol.convert_alpha().copy()
            vol.fill((255, 255, 255, self.volAlpha), None, pygame.BLEND_RGBA_MULT) 
            self.header.blit(vol, (25, (self.headerHeight - vol.get_height()) / 2))


        battery = Common.loadCachedImage(self.getCurrentBatteryImage())
        self.header.blit(battery, (440, (self.headerHeight - battery.get_height()) / 2))

             

    def getCurrentVolumeImage(self):
        self.readVolume()     
        if(self.vol == 0):
            return "theme/vol0.png"
        if(self.vol >= 0 and self.vol < 20):
            return "theme/vol1.png"
        if(self.vol >= 20 and self.vol < 40):
            return "theme/vol2.png"
        if(self.vol >= 40 and self.vol < 60):
            return "theme/vol3.png"
        if(self.vol >= 60 and self.vol < 80):
            return "theme/vol4.png"
        if(self.vol >= 80):
            return "theme/vol5.png"       

       

    def getCurrentBatteryImage(self):
        #TODO implement battery reading from device
        return "theme/battery_3.png"
    
    def getSDCardImage(self):
        #TODO implement battery reading from device
        return "theme/sdcard.png"

    def updateVolume(self):
        try:
            change = os.stat("/opt/volume/volume.cfg").st_mtime
            if(change != self.lastVolChange):
                self.lastVolChange = change
                if(self.volAnim != None):
                    TaskHandler.stopAnimation(self.volAnim)
                    self.volAlpha = 255
                    self.updateHeader()
                    RenderControl.setDirty()
               
                self.volAnim = TaskHandler.addAnimation(255, 0, 400, self.volumeAnimation, 2500) 
        except Exception as ex:
            pass

    def readVolume(self):
        if(self.volumeDevice == None):
            return

        try:
            self.volumeDevice.seek(0)
            first_line = self.volumeDevice.readline()
            self.vol = int(first_line)          
        except Exception as ex:
            pass
    
    def updateBattery(self):
        self.readBatteryLevel()

    def readBatteryLevel(self):
        if(self.battery == None):
            return

        try:
            self.battery.seek(0)
            first_line = self.battery.readline()
            batteryLevelMVolt = int(first_line)
          
            if (not "batteryLow" in self.config):
                self.config["batteryLow"] = 3600
                self.config["batteryHight"] = 4500

            if(batteryLevelMVolt < self.config["batteryLow"]):
                self.config["batteryLow"] = batteryLevelMVolt
            
            if(batteryLevelMVolt > self.config["batteryHight"]):
                self.config["batteryHigh"] = batteryLevelMVolt

            self.batteryLevel = (int(batteryLevelMVolt) - int(self.config["batteryLow"]) ) / ( int(self.config["batteryHight"]) -  int(self.config["batteryLow"]) )  * 100

        except Exception as ex:
            pass
    
    def volumeAnimation(self, start, target, current, finished):
        self.volAlpha = int(current)

        if(finished):
            self.volAlpha = 0
            self.volumeAnim = None
        
        self.updateHeader()
        RenderControl.setDirty()
    
    def __init__(self, height):
        self.headerHeight = height
        self.updateHeader()      

        try:
            self.battery = open("/proc/jz/battery", "r")
            self.volumeDevice = open("/opt/volume/volume.cfg", "r")
        except Exception as ex:
            print("Could not open devices" + str(ex))

        

        TaskHandler.addPeriodicTask(100, self.updateVolume)
        TaskHandler.addPeriodicTask(1000, self.updateBattery)
        TaskHandler.addAnimation(255, 0, 600, self.volumeAnimation, 2500) 
   
