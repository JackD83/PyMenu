# -*- coding: utf-8 -*-
import pygame, sys, Common, MainMenu, Configuration, RenderControl, TaskHandler,subprocess
import platform, Suspend

from pygame.locals import *



pygame.init()
pygame.font.init()
pygame.mouse.set_visible(False)
fpsClock = pygame.time.Clock()
pygame.key.set_repeat(50, 50)
config = Configuration.getConfiguration()

#reset to default clockspeed
try:
   subprocess.Popen(["/opt/overclock/overclock.dge", str(Common.CLOCKSPEED)])
except Exception as ex:
    pass

def setVolume():
    if(Configuration.isRS97()):
        try:
            pass
            ##not working
            # from fcntl import ioctl
       
            # filename = "/dev/mixer"
            # SOUND_MIXER_WRITE_VOLUME = 0xc0044d00
            # oss_volume = 100 | (100 << 8)
          
            # fd = open(filename, "wb")            
            # ioctl(fd, SOUND_MIXER_WRITE_VOLUME, oss_volume)
            # fd.close()
        except Exception as ex:
            print("could not set volume: " + str(ex))

def init():
    setVolume()
    if(Configuration.isRS97() and platform.processor() == ""):
        realScreen = pygame.display.set_mode((320,480), HWSURFACE, 16)
    else:
        realScreen = pygame.display.set_mode((config["screenWidth"],config["screenHeight"]), HWSURFACE, 16)

    screen = pygame.Surface((config["screenWidth"],config["screenHeight"]))

    renderObject = MainMenu.MainMenu(screen)

    suspend = Suspend.Suspend()
    
    while True: # main game loop
        events = pygame.event.get()       
        for event in events:
            if event.type == QUIT:
                pygame.quit()            
                sys.exit()

        suspend.handleEvents(events)
        renderObject.handleEvents(events)
        
        if(RenderControl.isDirty()):
            update(renderObject, screen,events)

            if(Configuration.isRS97() and platform.processor() == ""):
                realScreen.blit(pygame.transform.scale(screen, (320,480) ), (0,0))
            else:
                 realScreen.blit(screen, (0,0))

            pygame.display.update()
            RenderControl.setDirty(False)

        TaskHandler.updateTasks()
        fpsClock.tick(Common.FPS)


def update(renderObject, screen, events):  
    renderObject.render(screen)


init()