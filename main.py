import pygame, sys, common, MainMenu, Configuration
from pygame.locals import *


Configuration = ""


pygame.init()
pygame.font.init()
FPS = 30 # frames per second setting
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

        update(renderObject, screen,events)

        pygame.display.update()        
        fpsClock.tick(FPS)


def update(renderObject, screen, events):
    renderObject.handleEvents(events)
    renderObject.render(screen)


init()