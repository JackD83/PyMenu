# -*- coding: utf-8 -*-
import sys, Common, traceback, os

# catch global exception and try to enable usb
def except_hook(exctype, value, traceback):
    if(traceback != None):
       traceback.print_exception(exctype, value)

    Common.mountSD(True)
    Common.mountUSB()
    import time
    while True:
        time.sleep(1)
    
sys.excepthook = except_hook

import pygame, MainMenu, Configuration, RenderControl, TaskHandler
import Suspend, BrightnessVolumeControl
import time

from pygame.locals import *

textFont = pygame.font.Font('theme/NotoSans-Regular.ttf', 10)

print("PyGame Init")
pygame.init()
pygame.font.init()
pygame.mouse.set_visible(False)
fpsClock = pygame.time.Clock()
pygame.key.set_repeat(50, 50)
config = Configuration.getConfiguration()


def init():
    lastRenderTime = 1
    
    Common.mountSD(True)

    # try:
    #     if(not Configuration.isRG350()):
    #         os.system('/usr/bin/retrofw network on')
    # except Exception as ex:
    #     pass
    
    realScreen = pygame.display.set_mode((config["screenWidth"],config["screenHeight"]), HWSURFACE, 16)
    screen = pygame.Surface((config["screenWidth"],config["screenHeight"]))
    
    suspend = Suspend.Suspend()
    renderObject = MainMenu.MainMenu(screen, suspend)
   
    
    brightness = BrightnessVolumeControl.BrightnessVolume()

    
    while True: # main game loop
        events = pygame.event.get()       
        for event in events:
            if event.type == QUIT:
                pygame.quit()            
                sys.exit()

        suspend.handleEvents(events)
        renderObject.handleEvents(events)
        brightness.handleEvents(events)
        
        if(RenderControl.isDirty()):   
            start = int(round(time.time() * 1000))            
            RenderControl.setDirty(False)
            renderObject.render(screen)
            brightness.render(screen)

            if("showFPS" in config["options"] and config["options"]["showFPS"]):
                if(lastRenderTime == 0):
                    lastRenderTime = 1
                textSurface = textFont.render(str(int(round(1000/lastRenderTime))) + "fps ~" + str(lastRenderTime) + "ms", True, (255,255,255))
                screen.blit(textSurface, (0,0))
                #print("render time: " + str(lastRenderTime))
       
            realScreen.blit(screen, (0,0))
            
            
            pygame.display.update()
            lastRenderTime = int(round(time.time() * 1000))  - start
            

        TaskHandler.updateTasks()
        fpsClock.tick(Common.getFPS())
try:
    init()
except Exception as err:
    print(str(err))
    traceback.print_exc()
    except_hook(None, None, None)
