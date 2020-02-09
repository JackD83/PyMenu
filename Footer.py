import RenderObject, Configuration, Common
import os
import pygame, sys
import Theme

class Footer(RenderObject.RenderObject):
    config = Configuration.getConfiguration()
    theme = Configuration.getTheme()
    pygame.font.init()
    footerFont = pygame.font.Font('theme/NotoSans-Regular.ttf', 14)
    footerHeight = 24
    footer = None
    spacing = 6
    yPos = config["screenHeight"] - footerHeight
    enabled = True
    footerColor = None

    def getHeight(self):
        return self.footerHeight

    def setEnabled(self, enabled):
        self.enabled = enabled

    def setYPosition(self, yPos):
        self.yPos = yPos

    def render(self, screen):
        if(self.enabled):
            screen.blit(self.footer, (0,self.yPos ))

    def initFooter(self):
        self.footer = pygame.Surface((self.config["screenWidth"], self.footerHeight))
        self.footer.fill(self.footerColor)

        leftOffset = 10
        for entry in self.left:
            if(entry[0] != None):
                icon = Common.loadImage(entry[0])
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
                icon = Common.loadImage(entry[0])
                icon= icon.convert_alpha().copy()
                icon.fill(self.textColor, None, pygame.BLEND_RGBA_MULT)   
                self.footer.blit(icon, (rightOffset - icon.get_width() , (self.footerHeight - icon.get_height()) / 2))
                rightOffset = rightOffset - icon.get_width() - self.spacing
           
          
    def __init__(self,left,right, textColor, footerColor=(57,58,59)):
        self.left = left
        self.right = right
        self.textColor = textColor
        self.footerColor = footerColor

        self.initFooter()
      
