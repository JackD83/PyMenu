import RenderObject, Configuration
import os, Keys, RenderControl
import pygame, sys

class InfoOverlay(RenderObject.RenderObject):
    background = None
    config = Configuration.getConfiguration()

    def render(self, screen):

        screen.blit(self.background, (self.xOffset,self.yOffset))


    def handleEvents(self, events):    
        for event in events:    
            if event.type == pygame.KEYDOWN:
                if event.key == Keys.DINGOO_BUTTON_B or event.key == Keys.DINGOO_BUTTON_A:
                    self.callback(1)
                    RenderControl.setDirty()

    
    def __init__(self, image, callback):
        print("Opened Overlay menu ")
        self.callback = callback
        self.background = pygame.image.load(image)
        self.xOffset = (self.config["screenWidth"] - self.background.get_width()) / 2
        self.yOffset = (self.config["screenHeight"] - self.background.get_height()) / 2