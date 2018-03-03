import RenderObject, Configuration, SelectionMenu, FileChooser, EmuRunner
import os
import pygame, sys

class Header():
    config = Configuration.getConfiguration()
    theme = Configuration.getTheme()
    headerHeight = 30

    def render(self, screen):
        screen.blit(self.header, (0,0))

    
    def __init__(self):          
        self.header = pygame.Surface((self.config["screenWidth"], self.headerHeight),pygame.SRCALPHA)
        self.header.fill(Configuration.toColor(self.theme["header"]["color"]))
        batter = pygame.image.load("theme/battery_3.png")
        self.header.blit(batter, (420, 5))
   
