import pygame, sys, Common, MainMenu, Configuration, RenderControl, TaskHandler,subprocess

from pygame.locals import *


Configuration = ""


pygame.init()
pygame.font.init()
pygame.mouse.set_visible(False)
fpsClock = pygame.time.Clock()
pygame.key.set_repeat(50, 50)


#reset to default clockspeed
try:
   subprocess.Popen(["/opt/overclock/overclock.dge", str(Common.CLOCKSPEED)])
except Exception as ex:
    pass



def init():
    screen = pygame.display.set_mode((480, 272), 0, 16)
    renderObject = MainMenu.MainMenu(screen)
    
    while True: # main game loop
        events = pygame.event.get()       
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()       

        renderObject.handleEvents(events)
        if(RenderControl.isDirty()):
            update(renderObject, screen,events)
            pygame.display.update()
            RenderControl.setDirty(False)

        TaskHandler.updateTasks()
        fpsClock.tick(Common.FPS)


def update(renderObject, screen, events):  
    renderObject.render(screen)


init()