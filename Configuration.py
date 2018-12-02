import json, subprocess, os, copy,shutil, platform, pygame, Common
from ast import literal_eval as make_tuple
from pprint import pprint

configuration = None
theme = json.load(open('theme/theme.json'))
listeners = []

def getConfiguration():   
    if(configuration == None):      
        reloadConfiguration()

    return configuration

def reloadConfiguration(): 
    global configuration
    configuration = json.load(open('config/config.json'))
    configuration["mainMenu"] = []
    pygame.init()
    configuration["RS97"] = checkRS97()
    setResolution()

    if os.path.exists(os.path.dirname("config/main")):
        fileList = os.listdir("config/main")
        Common.quick_sort(fileList)       
        for name in fileList:
            try:                   
                entry = json.load(open("config/main/" + name + "/config.json"))
                entry["source"] = name
                configuration["mainMenu"].append(entry)
                if(entry["type"] == "native"):
                    entry["data"] = []
                    try:
                        itemlist =  os.listdir("config/main/" + name + "/items")
                        Common.quick_sort(itemlist) 
                        for itemName in itemlist:
                            item = json.load(open("config/main/" + name + "/items/" + itemName))
                            item["source"] = itemName
                            entry["data"].append(item)
                    except Exception as ex:
                        print(str(ex))

            except Exception as ex:
                print(str(ex))                  
   
def checkRS97():
    
    infoObject = pygame.display.Info()

    print("RS97 check " + str(infoObject.current_h))
    
    if(infoObject.current_h == 480):
        return True

    #windows platform
    elif(os.name == "nt"):
        return False

    return False    

def setResolution():
    global configuration
    infoObject = pygame.display.Info()
  
    if(checkRS97()):
        configuration["screenWidth"] = 320
        configuration["screenHeight"] = 240
    
    elif(infoObject.current_w == 480):
        configuration["screenWidth"] = 480
        configuration["screenHeight"] = 272
    
    #windows platform
    elif(os.name == "nt"):
        configuration["screenWidth"] = 320
        configuration["screenHeight"] = 240

def saveConfiguration():
    try:
        subprocess.Popen(["sync"])
    except Exception:
        pass
      
    try:
        shutil.rmtree("config/main") 
    except Exception as ex:
        print(str(ex))     
    
    allConfig = copy.deepcopy(configuration)
    main = allConfig["mainMenu"]
    allConfig.pop('mainMenu', None)

    with open('config/config.json', 'w') as fp: 
        json.dump(allConfig, fp,sort_keys=True, indent=4)

    for index, item in enumerate(main):
        if( "source" not in item):
            fileName = "config/main/" + str(index).zfill(3) + " " +  item["name"] + "/config.json" 
        else:
            fileName = "config/main/" + item["source"] + "/config.json"

        if(item["type"] == "native"):
            data = item["data"]
            item.pop('data', None)
            for dataIndex, dataItem in enumerate(data):
                if("source" not in dataItem):
                    dataName = "config/main/" + str(index).zfill(3) + " " +  item["name"] + "/items/" + str(dataIndex).zfill(3) + " " + dataItem["name"] + ".json"
                else:
                    dataName = "config/main/" + item["source"] + "/items/" + dataItem["source"]

                del dataItem["source"]
                storeConfigPart(dataName, dataItem)

        if(item["type"] != "lastPlayed"):
            del item["source"]
            storeConfigPart(fileName, item)

       
    for l in listeners:
        l()
       


def storeConfigPart(fileName, item):
    if not os.path.exists(os.path.dirname(fileName)):
        try:
            os.makedirs(os.path.dirname(fileName))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open(fileName, 'w') as fp: 
        json.dump(item, fp,sort_keys=True, indent=4)

        

def getTheme():
    return theme

def toColor(input):
    return make_tuple(input)

def isRS97():
    return "RS97" in configuration and configuration["RS97"]

def addConfigChangedCallback(listener):
    listeners.append(listener)


def getPathData(path, data = None):
    if(data == None):
        data = configuration

    if path and data:
        args = path.split("/")
        element  = args[0]
        if element:
            newPath = '/'.join(args[1:])
            value = data.get(element)
            return value if len(args) == 1 else getPathData(value, newPath)

