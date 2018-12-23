# -*- coding: utf-8 -*-
import pygame, sys, subprocess
import platform, json
import time, os

from pygame.locals import *

DINGOO_BUTTON_UP     =       pygame.K_UP
DINGOO_BUTTON_DOWN   =       pygame.K_DOWN
DINGOO_BUTTON_RIGHT  =       pygame.K_RIGHT
DINGOO_BUTTON_LEFT   =       pygame.K_LEFT
DINGOO_BUTTON_R      =       pygame.K_BACKSPACE
DINGOO_BUTTON_L      =       pygame.K_TAB
DINGOO_BUTTON_A      =       pygame.K_LCTRL
DINGOO_BUTTON_B      =       pygame.K_LALT
DINGOO_BUTTON_X      =       pygame.K_SPACE
DINGOO_BUTTON_Y      =       pygame.K_LSHIFT
DINGOO_BUTTON_SELECT =       pygame.K_ESCAPE
DINGOO_BUTTON_START  =       pygame.K_RETURN
DINGOO_BUTTON_END    =       pygame.K_UNKNOWN
DINGOO_BUTTON_VOL_UP =       pygame.K_2
DINGOO_BUTTON_VOL_DOWN =     pygame.K_1
DINGOO_BUTTON_BRIGHTNESS  =  pygame.K_3




pygame.init()
pygame.font.init()
pygame.mouse.set_visible(False)
fpsClock = pygame.time.Clock()

config = json.load(open('../config/config.json'))
textFont = pygame.font.Font('../theme/NotoSans-Regular.ttf', 10)

rs97ScreenFix =  config["RS97ScreenFix"] if "RS97ScreenFix" in config else None

#set screen mode
if("RS97" in config and config["RS97"] and not rs97ScreenFix):
    try:
        os.system('echo 2 > /proc/jz/lcd_a320')
    except Exception as ex:
        pass

class Updater():

    STATE = 0
    keepConfig = True

    def init(self):
    
        if("RS97" in config and config["RS97"] and not rs97ScreenFix):
            realScreen = pygame.display.set_mode((320,240), HWSURFACE, 16)
            screen = pygame.Surface((config["screenWidth"],config["screenHeight"]))
        elif("RS97" in config and config["RS97"] and rs97ScreenFix):
            print("setting 480 screen")
            realScreen = pygame.display.set_mode((320,480), HWSURFACE, 16)
            screen = pygame.Surface((config["screenWidth"],config["screenHeight"]))
        else:
            realScreen = pygame.display.set_mode((config["screenWidth"],config["screenHeight"]), HWSURFACE, 16)
            screen = pygame.Surface((config["screenWidth"],config["screenHeight"]))


        
        while True: # main game loop
            events = pygame.event.get()       
            for event in events:
                if event.type == QUIT:
                    pygame.quit()            
                    sys.exit()

            self.handleEvents(events)
            self.render(screen)

            if(rs97ScreenFix):
                screenFix = pygame.transform.scale(screen, (int(320),int(480)) )
                realScreen.blit(screenFix, (0,0))
                
            else:
                realScreen.blit(screen, (0,0))
            
            

            pygame.display.update()
                
            fpsClock.tick(30)

    def render(self, screen):
        screen.fill((0,0,0))

        if(self.STATE == 0):
            textSurface = textFont.render("Update PyMenu?   Press A to continue, B to abbort", True, (255,255,255))
            screen.blit(textSurface, (10,10))
        elif(self.STATE ==1):
            textSurface = textFont.render("Keep Configuration?   Press A to keep, B to override", True, (255,255,255))
            screen.blit(textSurface, (10,10))

    def handleEvents(self, events): 

        for event in events:    
            if event.type == pygame.KEYDOWN:  
                if event.key == DINGOO_BUTTON_A:
                    if(self.STATE == 0):
                        self.STATE = 1
                    elif(self.STATE == 1):
                        self.update()
                if event.key == DINGOO_BUTTON_B:
                    if(self.STATE == 0):
                        pygame.quit()            
                        sys.exit()
                    if(self.STATE == 1):
                        self.keepConfig = False
                        self.update()

    def update(self):
        print("updating py menue "  + str(self.keepConfig))


    def __init__(self):
        self.init()

Updater()