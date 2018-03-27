
import pygame, sys
import os.path

def loadImage(path): 

    if(os.path.exists(path)):
        try:
            return pygame.image.load(path)
        except Exception:
            print("Could not load image " + str(path) + " " + str(Exception))
            return  pygame.Surface((1,1),pygame.SRCALPHA)
      
    else:
        print("File not found " + str(path))

    return  pygame.Surface((1,1),pygame.SRCALPHA)

def aspect_scale(img, bx,by ):      
    ix,iy = img.get_size()
    if ix > iy:
        # fit to width
        scale_factor = bx/float(ix)
        sy = scale_factor * iy
        if sy > by:
            scale_factor = by/float(iy)
            sx = scale_factor * ix
            sy = by
        else:
            sx = bx
    else:
        # fit to height
        scale_factor = by/float(iy)
        sx = scale_factor * ix
        if sx > bx:
            scale_factor = bx/float(ix)
            sx = bx
            sy = scale_factor * iy
        else:
            sy = by

    return pygame.transform.scale(img, (int(sx),int(sy)) )