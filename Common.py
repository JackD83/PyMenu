
import pygame, sys, Configuration
import os, subprocess, platform
from threading import Thread


CLOCKSPEED = 628 #default clockspeed
imageCache = {}
gameList = {}


def loadGameListAsync():
    thread = Thread(target = loadGameList, args = ())
    thread.start()   


def loadGameList():
    global gameList
    gameList = {}
    try:
        with open("config/gamelist.txt") as f:
            lines = f.readlines() 
            for line in lines:
                try:
                    res = line.split("|")
                    gameList[res[1].strip() + ".zip"] = res[3].strip()    
                except Exception as ex:
                     print("Error adding game to list: " + line)               

       
    except Exception as ex:
        print("could not loa game list")
            
def getGameName(romName):
    global gameList
    if(romName in gameList and gameList[romName] != None):
        return gameList[romName]
    else:
        return romName


def loadImage(path): 

    if(path != None and os.path.exists(path)):
        try:
            return pygame.image.load(path)
        except Exception:
            print("Could not load image " + str(path) + " " + str(Exception))
            return  pygame.Surface((1,1),pygame.SRCALPHA)
      
    else:
        print("File not found " + str(path))

    return  pygame.Surface((1,1),pygame.SRCALPHA)

def getFPS():
    if(Configuration.isRS97() or platform.processor() == ""):
       return 30
    else:
       return 20



def loadCachedImage(path):
    global imageCache
    if(path in imageCache):
        return imageCache[path]
    else:
        image = loadImage(path)
        imageCache[path] = image
        return image

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

def mountSD(ext):
    try:
        if ext:
            cmd = "par=$(( $(readlink /tmp/.int_sd | head -c -3 | tail -c 1) ^ 1 )); par=$(ls /dev/mmcblk$par* | tail -n 1); sync; umount -fl /mnt/ext_sd; mount -t vfat -o rw,utf8 $par /mnt/ext_sd"
        else:
            cmd = "par=$(readlink /tmp/.int_sd | head -c -3 | tail -c 1); par=$(ls /dev/mmcblk$par* | tail -n 1); sync; umount -fl /mnt/int_sd; mount -t vfat -o rw,utf8 $par /mnt/int_sd"

        p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

    except Exception:
        pass

def umountSD(ext):
    try:
        if ext:
            cmd = "sync; umount -fl /mnt/ext_sd"
        else:
            cmd = "sync; umount -fl /mnt/int_sd"

        p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
    except Exception:
        pass

def mountUSB():
    try:
        umountSD(True)
        umountSD(False)

        intSD = "echo \"\" > /sys/devices/platform/musb_hdrc.0/gadget/gadget-lun1/file; par=$(readlink /tmp/.int_sd | head -c -3 | tail -c 1); par=$(ls /dev/mmcblk$par* | tail -n 1); echo \"$par\" > /sys/devices/platform/musb_hdrc.0/gadget/gadget-lun1/file"
        extSD = "echo \"\" > /sys/devices/platform/musb_hdrc.0/gadget/gadget-lun0/file; par=$(( $(readlink /tmp/.int_sd | head -c -3 | tail -c 1) ^ 1 )); par=$(ls /dev/mmcblk$par* | tail -n 1); echo \"$par\" > /sys/devices/platform/musb_hdrc.0/gadget/gadget-lun0/file"

        subprocess.Popen(intSD, shell=True, stderr=subprocess.PIPE)
        subprocess.Popen(extSD, shell=True, stderr=subprocess.PIPE)

    except Exception as ex:
        print("mount exception " + str(ex))

def blitMultilineText(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

def quick_sort(items):
        """ Implementation of quick sort """
        if len(items) > 1:
                pivot_index = int(len(items) / 2)
                smaller_items = []
                larger_items = []
 
                for i, val in enumerate(items):
                        if i != pivot_index:
                                if val < items[pivot_index]:
                                        smaller_items.append(val)
                                else:
                                        larger_items.append(val)
 
                quick_sort(smaller_items)
                quick_sort(larger_items)
                items[:] = smaller_items + [items[pivot_index]] + larger_items
