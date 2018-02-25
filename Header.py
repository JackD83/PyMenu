import RenderObject, Configuration, SelectionMenu, FileChooser, EmuRunner
import os
import pygame, sys

class Header():
    config = Configuration.getConfiguration()
    theme = Configuration.getTheme()
    headerHeight = 31

    def render(self, screen):
        screen.blit(self.header, (0,0))

    
    def __init__(self):          
        self.header = pygame.Surface((self.config["screenWidth"], self.headerHeight),pygame.SRCALPHA)
        self.header.fill(Configuration.toColor(self.theme["header"]["color"]))
   
