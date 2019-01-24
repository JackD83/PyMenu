import json, subprocess, os, copy,shutil, platform, pygame, Common
from ast import literal_eval as make_tuple
from pprint import pprint

configuration = None
theme = json.load(open('theme/theme.json'))
listeners = []
types = ["RS97", "RS07", "K3P"]

def getConfiguration():   
    if(configuration == None):      
        reloadConfiguration()

    return configuration

def reloadConfiguration(): 
    global configuration
    configuration = json.load(open('config/config.json'))
    if("version" not in configuration):
        configuration["version"] = "0"

    if("type" not in configuration["options"] or configuration["options"]["type"] not in types):
        print("forcing type to RS97")
        configuration["options"]["type"] = "RS97"

    if("themeName" not in configuration["options"]):
        configuration["options"]["themeName"] = "default"


    configuration["mainMenu"] = []
  
    setResolution()


    if os.path.exists(os.path.dirname("config/main/")):
        fileList = os.listdir("config/main/")
        Common.quick_sort(fileList)       
        for name in fileList:
            try:         
                if(os.path.isdir("config/main/" + name )):       
                    entry = json.load(open("config/main/" + name + "/config.json"))
                    entry["source"] = name
                    if("available" not in entry or configuration["options"]["type"] in entry["available"] or
                    configuration["options"]["showAll"] ):
                        appendTheme(entry)
                        configuration["mainMenu"].append(entry)
                       

                        if(entry["type"] == "native"):
                            entry["data"] = []
                            try:
                                itemlist =  os.listdir("config/main/" + name + "/items")
                                Common.quick_sort(itemlist) 
                                for itemName in itemlist:
                                    item = json.load(open("config/main/" + name + "/items/" + itemName))
                                    item["source"] = itemName
                                    appendTheme(item)
                                    entry["data"].append(item)

                                    
                            except Exception as ex:
                                print(str(ex))
                

            except Exception as ex:
                print(str(ex))  

    print("Load finished!!!")

def appendTheme(entry):
    themeName = configuration["options"]["themeName"]
    entryName = entry["name"]

    try:
        if os.path.exists("theme/" + themeName + "/" + entryName + ".json"):
            themeConfig = json.load(open("theme/" + themeName + "/" + entryName + ".json")) 
            entry.update(themeConfig)
        else:
            #print("loaded default config for " + entryName)
            if("type" in entry):
                #if it hast type param, its a main menu entry
               
                themeConfig = json.load(open("theme/default.json")) 
                entry.update(themeConfig)

            
    except Exception as ex:
        print(str(ex))

def saveTheme(entry):
    themeName = configuration["options"]["themeName"]
    entryName = entry["name"]
    try:
        theme = {}
        if "folderIcon" in entry:
            theme["folderIcon"] = entry["folderIcon"]
            del entry["folderIcon"]
        if "icon" in entry: 
            theme["icon"] = entry["icon"]
            del entry["icon"]
        if "background" in entry: 
            theme["background"] = entry["background"]
            del entry["background"]
        if "preview" in entry: 
            theme["preview"] = entry["preview"]
            del entry["preview"]

        if os.path.exists("theme/" + themeName + "/" + entryName + ".json"):
            #print("Duplicate name! " + str(entryName) )
            pass

        with open("theme/" + themeName + "/" + entryName + ".json", 'w') as fp: 
            json.dump(theme, fp,sort_keys=True, indent=4) 


    except Exception as ex:
        print(str(ex))

   




def setResolution():
    global configuration
   
    if(isRS97()):
        configuration["screenWidth"] = 320
        configuration["screenHeight"] = 240
    
    #RS07 & K3P
    else:
        configuration["screenWidth"] = 480
        configuration["screenHeight"] = 272
    
    #windows platform or mac
    if(platform.processor() != ""):
        configuration["screenWidth"] = 320
        configuration["screenHeight"] = 240


def saveConfiguration():
        

    print("saving")
    try:
        subprocess.Popen(["sync"])
    except Exception:
        pass
         
    
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

                if "source" in dataItem: del dataItem["source"]
                storeConfigPart(dataName, dataItem)
                saveTheme(dataItem)

        if(item["type"] != "lastPlayed"):
            if "source" in item: del item["source"]
            saveTheme(item)
            storeConfigPart(fileName, item)
        elif(item["type"] == "lastPlayed"):
            dataName = "config/" + "main" + "/lastPlayed.json"
            if("data" in item): del item["data"]
            saveTheme(item)
            storeConfigPart(dataName, item)

       
    for l in listeners:
        l()

    print("Save finished")
       


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
    return "type" in configuration["options"] and configuration["options"]["type"] == "RS97"

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

