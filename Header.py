import RenderObject, Configuration, SelectionMenu, FileChooser, Runner, TaskHandler
import os, Common, RenderControl
import pygame, sys

class Header():
    config = Configuration.getConfiguration()
    theme = Configuration.getTheme()
    headerHeight = 24
    
    battery = None

    
    batteryLevel = 0
    currentBatteryImage = None

    usbDevice = None
  

    def render(self, screen):
        screen.blit(self.header, (0,0))

    def updateHeader(self):
        self.header = pygame.Surface((self.config["screenWidth"], self.headerHeight),pygame.SRCALPHA)
        self.header.fill(Configuration.toColor(self.theme["header"]["color"]))

        self.currentBatteryImage = self.getCurrentBatteryImage()

        battery = Common.loadCachedImage(self.currentBatteryImage)
        self.header.blit(battery, (self.config["screenWidth"] - 40, (self.headerHeight - battery.get_height()) / 2))

                

    def getCurrentBatteryImage(self):
        if(self.isUsbConnected()):
            return "theme/battery_charging.png"

        if(self.batteryLevel == 0):
            return "theme/battery_0.png"
        if(self.batteryLevel >= 0 and self.batteryLevel < 20):
            return "theme/battery_1.png"
        if(self.batteryLevel >= 20 and self.batteryLevel < 60):
            return "theme/battery_2.png"
        if(self.batteryLevel >= 60):
            return "theme/battery_3.png"               
        
    def isUsbConnected(self):
        if(self.usbDevice == None):
            return False

        try:
            self.usbDevice.seek(0)
            first_line = self.usbDevice.readline().strip()         

            if(first_line == "usb"):
                return True      
        except Exception as ex:
            print(str(ex))
        
        return False
    
    def updateBattery(self):      
        self.readBatteryLevel()

        if(self.currentBatteryImage != self.getCurrentBatteryImage()):
            self.updateHeader()
            RenderControl.setDirty()

    def readBatteryLevel(self):
        if(self.battery == None):          
            return

        try:
            self.battery.seek(0)
            first_line = self.battery.readline()
            batteryLevelMVolt = int(first_line)
          
            if (not "batteryLow" in self.config):
                self.config["batteryLow"] = 3900
                self.config["batteryHigh"] = 4500

            if(batteryLevelMVolt < self.config["batteryLow"]):
                self.config["batteryLow"] = batteryLevelMVolt
            
            if(batteryLevelMVolt > self.config["batteryHigh"] and batteryLevelMVolt < 10000 ):
                self.config["batteryHigh"] = batteryLevelMVolt

            self.batteryLevel = float( (int(batteryLevelMVolt) - int(self.config["batteryLow"]) ) ) / float( ( int(self.config["batteryHigh"]) -  int(self.config["batteryLow"]) ) )  * 100.0

        except Exception as ex:
            print(str(ex))   
    
    
    def __init__(self, height):
        self.headerHeight = height
        self.updateHeader()      

        try:

            if(not Configuration.isRG350()):
                self.usbDevice = open("/sys/devices/platform/musb_hdrc.0/uh_cable", "r")
            
            if(Configuration.isRG350()):
                self.battery = open("/sys/class/power_supply/battery/voltage_now", "r")
            else:
                self.battery = open("/proc/jz/battery", "r")    



               
         
            self.updateBattery()
        except Exception as ex:
            print("Could not open devices" + str(ex))

        TaskHandler.addPeriodicTask(1000, self.updateBattery)
    
      
   
