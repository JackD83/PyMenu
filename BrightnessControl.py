import pygame, sys, Common, TaskHandler, Configuration
import os,subprocess, RenderObject, Keys,RenderControl

class Brightness(RenderObject.RenderObject):
    config = Configuration.getConfiguration()
    lcd_backlight = None

    textFont = pygame.font.Font('theme/NotoSansSymbols-Regular.ttf', 19)
 
    brightSymbol = textFont.render(u"\u26ef", True, (255,255,255))
   

    BRIGHTNESS_LEVELS = [10,30,50,70,100]
    brightnessIndex = 0

    showBrightness = False
    brightnessAlpha = 255

    width = 200
    height = 30

    animationId = None
    

    def render(self, screen):
        if(self.showBrightness):
            brightness = pygame.Surface((self.width + 4, self.height + 4),pygame.SRCALPHA)

            backgroundShadow = pygame.Surface(((self.width,self.height)),pygame.SRCALPHA)
            backgroundShadow.fill((0,0,0, 120))
            brightness.blit(backgroundShadow, (4,4))

            background = pygame.Surface((self.width,self.height),pygame.SRCALPHA)
            background.fill((137,137,137, 255))
              

            barWidth =  (self.width - 40) / len(self.BRIGHTNESS_LEVELS) * self.brightnessIndex
            if(self.brightnessIndex == 0):
                barWidth = 5         

            bar = pygame.Surface((barWidth,10))
            bar.fill((255,255,255, 255))

            x = (self.config["screenWidth"] - self.width + 2) / 2
            background.blit(bar, (50,10))

            background.blit(self.brightSymbol, (12,-5)) 
            
            brightness.blit(background, (0,0)) 

            brightnessCopy = brightness.convert_alpha().copy()

            brightnessCopy.fill((255, 255, 255, self.brightnessAlpha), None, pygame.BLEND_RGBA_MULT)

            screen.blit(brightnessCopy, (x,20))

    def animationCallback(self, start, target, current, finished):
        self.brightnessAlpha = current

        if(finished):
            self.showBrightness = False

        RenderControl.setDirty()    


    def handleEvents(self, events):     
        for event in events:    
            if event.type == pygame.KEYDOWN:         
                if event.key == Keys.DINGOO_BUTTON_BRIGHTNESS:
                    self.adjustBrightness()                                    
                
    def adjustBrightness(self):
        self.brightnessIndex = self.brightnessIndex + 1
        if(self.brightnessIndex >= len(self.BRIGHTNESS_LEVELS)):
            self.brightnessIndex = 0

        level = self.BRIGHTNESS_LEVELS[self.brightnessIndex]       
        self.setBrightness(level)        

        self.showBrightness = True
        self.brightnessAlpha = 255
      

        if(self.animationId is not None):
            TaskHandler.stopAnimation(self.animationId)            

        self.animationId = TaskHandler.addAnimation(255, 20, 600, self.animationCallback, 1500)
        
        RenderControl.setDirty()

    def setBrightness(self, level, store=True):
        
        #os.system('echo ' + str(level)  +  ' > /proc/jz/lcd_backlight')
        if(self.lcd_backlight is not None):
            self.lcd_backlight.write(str(level) + '\n')

        if(store):
            self.config["lcd_backlight"] = level
            Configuration.saveConfiguration()



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

