import RenderObject, Configuration, Common
import os, Keys, RenderControl
import pygame, sys

class ConfirmOverlay(RenderObject.RenderObject):
    background = None
    config = Configuration.getConfiguration()
    theme = Configuration.getTheme()
    entryFont = pygame.font.Font('theme/NotoSans-Regular.ttf', 16)
    footerHeight = 24
    spacing = 6
       

    def render(self, screen):
        screen.blit(self.background, (self.xOffset,self.yOffset))

    def initBackground(self):

        self.background = pygame.Surface((160, 110),pygame.SRCALPHA)
        self.background.fill((0,0,0))

        text = self.entryFont.render(self.text, True, self.textColor)
        xText =  ( self.background.get_width() - text.get_width()) / 2
        yText = (self.background.get_height() - text.get_height()) / 2
        self.background.blit(text, (xText,yText))

        self.xOffset = (self.config["screenWidth"] - self.background.get_width()) / 2
        self.yOffset = (self.config["screenHeight"] - self.background.get_height()) / 2

        footerOffset = self.background.get_height() - self.footerHeight
        
        rightOffset =  self.background.get_width() - 2
        for entry in self.buttons:
            if(entry[1] != None):
                text = self.entryFont.render(entry[1], True, self.textColor)
                self.background.blit(text, (rightOffset - text.get_width(),((self.footerHeight - text.get_height()) / 2) + footerOffset))
                rightOffset = rightOffset - text.get_width() - self.spacing
            if(entry[0] != None):
                icon = Common.loadImage(entry[0])
                self.background.blit(icon, (rightOffset - icon.get_width() , ((self.footerHeight - icon.get_height()) / 2) + footerOffset ))
                rightOffset = rightOffset - icon.get_width() - self.spacing


    def handleEvents(self, events):    
        for event in events:    
            if event.type == pygame.KEYDOWN:
                if event.key == Keys.DINGOO_BUTTON_B:
                    self.callback(-1)
                    RenderControl.setDirty()
                if event.key == Keys.DINGOO_BUTTON_A:
                    self.callback(1)
                    RenderControl.setDirty()

    
    def __init__(self, text, textColor,buttons, callback):      
        self.callback = callback
        self.text = text
        self.textColor = textColor
        self.buttons = buttons
        self.initBackground()
      