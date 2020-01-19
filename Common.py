
import pygame, sys, Configuration
import os, subprocess, platform
from threading import Thread
import json
import copy


CLOCKSPEED = 628 #default clockspeed
imageCache = {}
gameList = {}
isLoaded = False
hasLibopk = False

try:
    import OPK as opk
    hasLibopk = True
except Exception:
    print("OPK icons not supported")
           

def loadGameListAsync():
    thread = Thread(target = loadGameList, args = ())
    thread.start()   

def loadGameList():
    global gameList
    global isLoaded

    if(isLoaded):
        return

    isLoaded = True
    try:
        print("Loading game list")
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
    
def clearLastPlayed():
    try:
        lastPlayed = json.load(open("config/lastPlayedData.json"))
        del lastPlayed["data"][:]
        with open('config/lastPlayedData.json', 'w') as fp: 
            json.dump(lastPlayed, fp,sort_keys=True, indent=4)
    except Exception as ex:
        print("Exception " + str(ex))
            
def getGameName(romName):
    global gameList
    if(romName in gameList and gameList[romName] != None):
        return gameList[romName]
    else:
        return romName


def loadImage(path): 

    if(path != None and "opk#" in path.lower()):
        if(not hasLibopk):
            print("OPK icon not available")
            return  pygame.Surface((1,1),pygame.SRCALPHA)

        try:
            splitPath = path.split("#")

            try:
                icon = opk.extract_file(str(splitPath[0]), str(splitPath[1]))
                iconFile = open("/tmp/iconCache/" + splitPath[1] , "wb")
                iconFile.write(icon.getvalue())
                iconFile.close()
                
            except Exception as ex:
                print("Could not load OPK Icon " + str(ex))

            return pygame.image.load("/tmp/iconCache/" + splitPath[1] )

        except Exception:
            print("Could not load image " + str(path) + " " + str(Exception))
            return  pygame.Surface((1,1),pygame.SRCALPHA)


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

def aspect_scale(img, bx,by, upscale=True ):      
    ix,iy = img.get_size()

    if not upscale and ix < bx and iy < by:
        return img

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
    pass

def umountSD(ext):
    pass

def mountUSB():
    if(platform.processor() != ""):
        return


    try:     
        fileName = "run"  
        file = open("/tmp/" + fileName,"w")
        file.write("#!/bin/sh\n")

        file.write("/usr/bin/retrofw stop\n")       
        file.write("/usr/bin/retrofw storage\n")       
        sys.exit()

    except Exception as ex:
        print("mount exception " + str(ex))


def startNetwork():
    if(platform.processor() != ""):
        return

    try:     
        fileName = "run"  
        file = open("/tmp/" + fileName,"w")
        file.write("#!/bin/sh\n")

        file.write("/usr/bin/retrofw stop\n")       
        file.write("/usr/bin/retrofw network on\n")       
        sys.exit()

    except Exception as ex:
        print("mount exception " + str(ex))

def gmenu2x():
    try:     
        fileName = "run"  
        file = open("/tmp/" + fileName,"w")
        file.write("#!/bin/sh\n")
        file.write("cd /home/retrofw/apps/gmenu2x\n")     
        file.write("./gmenu2x\n")     

        sys.exit()

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

def addToCustomList(config, rom, dataName, limitEntries = True):
    data = getDataEntry(config, rom)

    try:
        listData = json.load(open("config/" + dataName + ".json"))
    
        last = listContains(listData, data)
        if(   last != None ):            
            listData["data"].remove(last)          


        listData["data"].insert(0, data)
        if(limitEntries):
            listData["data"] = listData["data"][0:20]

        with open("config/" +  dataName + ".json", 'w') as fp: 
            json.dump(listData, fp,sort_keys=True, indent=4)

        
    except Exception as ex:
        print("Exception " + str(ex))       

def getDataEntry(config, rom):
    data = copy.deepcopy(config)

    if(not rom == None):        
        filename_w_ext = os.path.basename(rom)
        filename, file_extension = os.path.splitext(filename_w_ext)

        if("fileFilter" in config):
            if any(file_extension in s for s in config["fileFilter"]):
                data["name"] = filename
            else:
                data["name"] = filename_w_ext
        else:
            data["name"] = filename_w_ext

        if("gameListName" in data):
            data["name"] = data["gameListName"]
            
        elif("useGamelist" in config and config["useGamelist"] == True):
            data["name"] = getGameName(filename_w_ext)
            data["gameListName"] = data["name"]
           
        data["rom"] = rom
        data["type"] = "emulator"

        if(not "preview" in data):
            data["preview"] = ""

        if("previews" in config and not config["previews"] == None):
             data["preview"] = str(config["previews"]) + "/" + str(filename) + ".png"

    else:
        data["type"] = "native"   

        
    return data

def listContains(list, data):
    for last in list["data"]:
        if( (data["type"] == "emulator" and last["type"] == "emulator" and last["rom"] == data["rom"]) or (data["type"] == "native" and last["type"] == "native" and last["cmd"] == data["cmd"]) ):   
     
            return last
          
    return None

def isFavourite(config, rom):
    conf = Configuration.getConfiguration()
    for entry in conf["mainMenu"]:
        if(entry["type"] == "favourites"):
            res = listContains(entry, getDataEntry(config,rom))
            if(res != None):
                return True
    
    return False


def addFavourite(config, rom):
    addToCustomList(config,rom, "favourites", False)
    
    #add to main menu favourites entry directly
    conf = Configuration.getConfiguration()
    for entry in conf["mainMenu"]:
        if(entry["type"] == "favourites"):
            newData = getDataEntry(config,rom)
            res = listContains(entry,newData)
            if(   res != None ):            
                entry["data"].remove(res)          

            entry["data"].insert(0, newData)


def removeFavourite(config, rom):
    dataName = "favourites"
    data = getDataEntry(config, rom)

    try:
        listData = json.load(open("config/" + dataName + ".json"))
    
        last = listContains(listData, data)
        if(   last != None ):            
            listData["data"].remove(last)          

        with open("config/" +  dataName + ".json", 'w') as fp: 
            json.dump(listData, fp,sort_keys=True, indent=4)

        
    except Exception as ex:
        print("Exception " + str(ex)) 

    #remove from  main menu favourites entry directly
    conf = Configuration.getConfiguration()
    for entry in conf["mainMenu"]:
        if(entry["type"] == "favourites"):
            
            res = listContains(entry,data)
            if( res != None ):            
                entry["data"].remove(res) 

def removeFavouriteData(data):
    dataName = "favourites"
  
    try:
        listData = json.load(open("config/" + dataName + ".json"))
    
        last = listContains(listData, data)
        if(   last != None ):            
            listData["data"].remove(last)          

        with open("config/" +  dataName + ".json", 'w') as fp: 
            json.dump(listData, fp,sort_keys=True, indent=4)

        
    except Exception as ex:
        print("Exception " + str(ex)) 

def removeOptionsEntries(list, remove):
    res = []
    for  entry in list:
        if("id" in entry and entry["id"] not in remove):
            res.append(entry)
    
    return res
            

