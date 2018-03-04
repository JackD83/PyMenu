import RenderObject, Configuration, SelectionMenu, FileChooser, EmuRunner
import os
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

        battery = pygame.image.load(self.getCurrentBatteryImage())
        self.header.blit(battery, (436, (self.headerHeight - battery.get_height()) / 2))

        vol = pygame.image.load(self.getCurrentVolumeImage())
        self.header.blit(vol, (380, (self.headerHeight - vol.get_height()) / 2))

        sdImage = self.getSDCardImage()
        if(sdImage != None):
            sd = pygame.image.load(sdImage)
            self.header.blit(sd, (350, (self.headerHeight - sd.get_height()) / 2))

    def getCurrentVolumeImage(self):
        #TODO implement volume reading from device
        return "theme/vol_5.png"

    def getCurrentBatteryImage(self):
        #TODO implement battery reading from device
        return "theme/battery_3.png"
    
    def getSDCardImage(self):
        #TODO implement battery reading from device
        return "theme/sdcard.png"

    
    def __init__(self, height):
        self.headerHeight = height
        self.updateHeader()

        
   
