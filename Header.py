import RenderObject, Configuration, SelectionMenu, FileChooser, Runner, TaskHandler
import os, Common
import pygame, sys

class Header():
    config = Configuration.getConfiguration()
    theme = Configuration.getTheme()
    headerHeight = 24

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
        #TODO implement volume reading from device
        return "theme/vol5.png"

    def getCurrentBatteryImage(self):
        #TODO implement battery reading from device
        return "theme/battery_3.png"
    
    def getSDCardImage(self):
        #TODO implement battery reading from device
        return "theme/sdcard.png"

    def updateVolume(self):
        pass
    
    def updateBattery(self):
        pass
    
    def __init__(self, height):
        self.headerHeight = height
        self.updateHeader()

        TaskHandler.addPeriodicTask(200, self.updateVolume)
        TaskHandler.addPeriodicTask(1000, self.updateBattery)      
   
