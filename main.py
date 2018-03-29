import pygame, sys, Common, MainMenu, Configuration, RenderControl, TaskHandler
from pygame.locals import *


Configuration = ""


pygame.init()
pygame.font.init()

fpsClock = pygame.time.Clock()
pygame.key.set_repeat(50, 50)


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