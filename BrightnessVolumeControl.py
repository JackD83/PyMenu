import pygame, sys, Common, TaskHandler, Configuration
import os,subprocess, RenderObject, Keys,RenderControl
from threading import Thread

class BrightnessVolume(RenderObject.RenderObject):
    config = Configuration.getConfiguration()
    lcd_backlight = None

    textFont = pygame.font.Font('theme/NotoSansSymbols-Regular.ttf', 19) 
    brightSymbol = textFont.render(u"\u26ef", True, (255,255,255))
    volSymbol = Common.loadCachedImage("theme/speaker.png")

    BRIGHTNESS_LEVELS = [10,30,50,70,100]
    brightnessIndex = 0
    VOLUME_LEVELS = [0,51,102,153,204,255]
    volumeIndex = 0

    showBrightness = False
    showVolume = False

    menuAlpha = 255

    currentVolumeLevel = 0

    width = 200
    height = 30

    animationId = None
    

    def render(self, screen):
        if(self.showBrightness or self.showVolume):
            overlay = pygame.Surface((self.width + 4, self.height + 4),pygame.SRCALPHA)

            backgroundShadow = pygame.Surface(((self.width,self.height)),pygame.SRCALPHA)
            backgroundShadow.fill((0,0,0, 120))
            overlay.blit(backgroundShadow, (4,4))

            background = pygame.Surface((self.width,self.height),pygame.SRCALPHA)
            background.fill((137,137,137, 255))
              

            if(self.showBrightness):
                barWidth =  (self.width - 40) / len(self.BRIGHTNESS_LEVELS) * self.brightnessIndex
                if(self.brightnessIndex == 0):
                    barWidth = 5  
            else:
                barWidth =  (self.width - 40) / len(self.VOLUME_LEVELS) * self.volumeIndex
                if(self.volumeIndex == 0):
                    barWidth = 5         

            bar = pygame.Surface((barWidth,10))
            bar.fill((255,255,255, 255))

            x = (self.config["screenWidth"] - self.width + 2) / 2
            background.blit(bar, (50,10))

            if(self.showBrightness):
                background.blit(self.brightSymbol, (12,-5)) 
            else:
                background.blit(self.volSymbol, (15,11))                 
            
            overlay.blit(background, (0,0)) 

            overlayCopy = overlay.convert_alpha().copy()

            overlayCopy.fill((255, 255, 255, self.menuAlpha), None, pygame.BLEND_RGBA_MULT)

            screen.blit(overlayCopy, (x,20))

    def animationCallback(self, start, target, current, finished):
        self.menuAlpha = current

        if(finished):
            self.showBrightness = False
            self.showVolume = False

        RenderControl.setDirty()    


    def handleEvents(self, events):     
        for event in events:    
            if event.type == pygame.KEYUP:         
                if event.key == Keys.DINGOO_BUTTON_BRIGHTNESS:
                    self.adjustBrightness()
                if event.key == Keys.DINGOO_BUTTON_VOL_DOWN:
                    self.volumeDown()
                if event.key == Keys.DINGOO_BUTTON_VOL_UP:
                    self.volumeUp()         

    def volumeUp(self):
        self.volumeIndex = self.volumeIndex + 1
        if(self.volumeIndex >= len(self.VOLUME_LEVELS)):
            self.volumeIndex = len(self.VOLUME_LEVELS) - 1

        self.currentVolumeLevel = self.VOLUME_LEVELS[self.volumeIndex]
        self.showVolume = True
        self.showBrightness = False

        self.config["volume"] = self.currentVolumeLevel
        Configuration.saveConfiguration()

        self.resetAnimation()

    def volumeDown(self):
        self.volumeIndex = self.volumeIndex -1
        if(self.volumeIndex < 0):
            self.volumeIndex = 0

        self.currentVolumeLevel = self.VOLUME_LEVELS[self.volumeIndex]
        self.showVolume = True
        self.showBrightness = False

        self.config["volume"] = self.currentVolumeLevel
        Configuration.saveConfiguration()

        self.resetAnimation()

    def resetAnimation(self):
        self.menuAlpha = 255
        if(self.animationId is not None):
            TaskHandler.stopAnimation(self.animationId)            

        self.animationId = TaskHandler.addAnimation(255, 20, 600, self.animationCallback, 1500)
        
        RenderControl.setDirty()
      
                
    def adjustBrightness(self):
        self.brightnessIndex = self.brightnessIndex + 1
        if(self.brightnessIndex >= len(self.BRIGHTNESS_LEVELS)):
            self.brightnessIndex = 0

        level = self.BRIGHTNESS_LEVELS[self.brightnessIndex]    
        thread = Thread(target = self.setBrightness, args = (level,))
        thread.start()     
            

        self.showBrightness = True
        self.showVolume = False
       
        self.resetAnimation()
       

    def setBrightness(self, level, store=True):
        print("Setting brightness " + str(level))
        
        #os.system('echo ' + str(level)  +  ' > /proc/jz/lcd_backlight')
        if(self.lcd_backlight is not None):
            self.lcd_backlight.seek(0)
            self.lcd_backlight.write(str(level) + '\n')
            self.lcd_backlight.flush()

        if(store):
            self.config["lcd_backlight"] = level
            Configuration.saveConfiguration()

    def initVolume(self):
        if("volume" in self.config and self.config["volume"] in self.VOLUME_LEVELS):
            self.volumeIndex = self.VOLUME_LEVELS.index(self.config["volume"])        
            print("restoring volume")  
        else:
            self.config["volume"] = 255
            Configuration.saveConfiguration()

        self.volumeIndex = self.VOLUME_LEVELS.index(self.config["volume"])
        self.currentVolumeLevel = self.VOLUME_LEVELS[self.volumeIndex]

        os.system('setVolume ' + str(self.currentVolumeLevel))


    def __init__(self):
        if("lcd_backlight" in self.config and self.config["lcd_backlight"] in self.BRIGHTNESS_LEVELS):
            self.brightnessIndex = self.BRIGHTNESS_LEVELS.index(self.config["lcd_backlight"])
            self.setBrightness(self.config["lcd_backlight"], False)        
        else:
            self.setBrightness(30)

        try:
            self.lcd_backlight = open("/proc/jz/lcd_backlight", "w")
        except Exception as identifier:
            print("Could not open lcd_backlight:" + str(identifier))

        self.initVolume()

