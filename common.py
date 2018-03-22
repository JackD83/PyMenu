
import pygame, sys
import os.path

def loadImage(path):
    print("Loading image " + path)

    if(os.path.exists(path)):
        try:
            return pygame.image.load(path)
        except Exception:
            print("Could not load image " + str(path) + " " + str(Error))
            return  pygame.Surface((1,1),pygame.SRCALPHA)
      
    else:
        print("File not found " + str(path))

    return  pygame.Surface((1,1),pygame.SRCALPHA)