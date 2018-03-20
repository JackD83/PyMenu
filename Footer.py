import RenderObject, Configuration
import os
import pygame, sys

class Footer(RenderObject.RenderObject):
    config = Configuration.getConfiguration()
    theme = Configuration.getTheme()
    pygame.font.init()
    footerFont = pygame.font.Font('theme/FreeSans.ttf', 14)
    footerHeight = 24
    footer = None
    spacing = 6

    def getHeight(self):
        return self.footerHeight

    def render(self, screen):
        screen.blit(self.footer, (0,self.config["screenHeight"] - self.footerHeight ))

    def initFooter(self):
        self.footer = pygame.Surface((self.config["screenWidth"], self.footerHeight),pygame.SRCALPHA)
        self.footer.fill(Configuration.toColor(self.theme["footer"]["color"]))

        leftOffset = 10
        for entry in self.left:
            if(entry[0] != None):
                icon = pygame.image.load(entry[0])
                self.footer.blit(icon, (leftOffset , (self.footerHeight - icon.get_height()) / 2))
                leftOffset = leftOffset + icon.get_width() + self.spacing
            if(entry[1] != None):
                text = self.footerFont.render(entry[1], True, self.textColor)
                self.footer.blit(text, (leftOffset,(self.footerHeight - text.get_height()) / 2))
                leftOffset = leftOffset + text.get_width() + self.spacing
        

        rightOffset = self.config["screenWidth"] - 10 
        for entry in self.right:
            if(entry[1] != None):
                text = self.footerFont.render(entry[1], True, self.textColor)
                self.footer.blit(text, (rightOffset - text.get_width(),(self.footerHeight - text.get_height()) / 2))
                rightOffset = rightOffset - text.get_width() - self.spacing
            if(entry[0] != None):
                icon = pygame.image.load(entry[0])
                self.footer.blit(icon, (rightOffset - icon.get_width() , (self.footerHeight - icon.get_height()) / 2))
                rightOffset = rightOffset - icon.get_width() - self.spacing
           
          
    def __init__(self,left,right, textColor):
        self.left = left
        self.right = right
        self.textColor = textColor

        self.initFooter()
      
