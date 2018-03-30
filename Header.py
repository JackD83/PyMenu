import RenderObject, Configuration, SelectionMenu, FileChooser, Runner, TaskHandler
import os, Common, RenderControl
import pygame, sys

class Header():
    config = Configuration.getConfiguration()
    theme = Configuration.getTheme()
    headerHeight = 24
    lastVolChange = 0
    vol = 0
  

    def render(self, screen):
        screen.blit(self.header, (0,0))

    def updateHeader(self):
        self.header = pygame.Surface((self.config["screenWidth"], self.headerHeight),pygame.SRCALPHA)
        self.header.fill(Configuration.toColor(self.theme["header"]["color"]))

        speaker = Common.loadImage("theme/speaker.png")      
        self.header.blit(speaker, (10, (self.headerHeight - speaker.get_height()) / 2))
       

        vol = Common.loadImage(self.getCurrentVolumeImage())      
        self.header.blit(vol, (25, (self.headerHeight - vol.get_height()) / 2))


        battery = Common.loadImage(self.getCurrentBatteryImage())
        self.header.blit(battery, (440, (self.headerHeight - battery.get_height()) / 2))

             

    def getCurrentVolumeImage(self):       
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
        change = os.stat("/opt/volume/volume.cfg").st_mtime
        if(change != self.lastVolChange):
            self.lastVolChange = change
            print("volume changed")
            self.readVolume()
            self.updateHeader()
            RenderControl.setDirty()

    def readVolume(self):
        with open("/opt/volume/volume.cfg") as f:
            first_line = f.readline()
            self.vol = int(first_line)
            print("read volume = " + str(self.vol))
        
    
    def updateBattery(self):
        pass
    
    def __init__(self, height):
        self.headerHeight = height
        self.updateHeader()      

        TaskHandler.addPeriodicTask(50, self.updateVolume)
        TaskHandler.addPeriodicTask(1000, self.updateBattery)      
   
