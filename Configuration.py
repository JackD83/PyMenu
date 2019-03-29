import json
import subprocess
import os
import copy
import shutil
import platform
import pygame
import Common
from ast import literal_eval as make_tuple
from pprint import pprint
import traceback


configuration = None
theme = json.load(open('theme/theme.json'))
listeners = []
types = ["RS97", "RS07", "K3P"]

currentTheme = {}


def getConfiguration():
    if(configuration == None):
        reloadConfiguration()

    return configuration


def reloadConfiguration(upgrade=True):
    global configuration
    global currentTheme

    configuration = json.load(open('config/config.json'))

   

    if("version" not in configuration):
        configuration["version"] = "0"

    if("type" not in configuration or configuration["type"] not in types):
        print("forcing type to RS97")
        configuration["type"] = "RS97"

    if("themeName" not in configuration["options"]):
        configuration["options"]["themeName"] = "default"

    try:
        currentTheme = json.load(
            open("theme/themes/" + configuration["options"]["themeName"] + ".json"))
    except Exception as ex:
        currentTheme = {}
        print("Could not load theme json" +
              str(configuration["options"]["themeName"]))

    setResolution()

    for entry in configuration["mainMenu"]:
        try:
            if(entry["type"] == "native"):
                entry["data"] = []
                entry["visible"] = True

                appendTheme(entry)

                try:
                    itemlist = os.listdir(entry["linkPath"])
                    Common.quick_sort(itemlist)

                    for itemName in itemlist:
                        item = createNativeItem(
                            entry["linkPath"] + "/" + itemName)
                        appendTheme(item)
                        entry["data"].append(item)

                except Exception as ex:
                    print("Error loading item:" + str(ex))
                    # traceback.print_exc()
            elif(entry["type"] == "lastPlayed"):
                entry["data"] = []
                entry["visible"] = "showLastPlayed" in configuration["options"] and configuration["options"]["showLastPlayed"]
                appendTheme(entry)

                try:
                    if(os.path.exists("config/lastPlayedData.json")):
                        lastPlayedData = json.load(
                            open("config/lastPlayedData.json"))
                        entry["data"] = lastPlayedData["data"]
                    else:
                        newData = {}
                        newData["data"] = []
                        entry["data"] = []
                        with open('config/lastPlayedData.json', 'w') as fp:
                            json.dump(newData, fp, sort_keys=True, indent=4)

                except Exception as ex:
                    print("Error loading last played")

            elif(hasConfig(entry["system"])):
                appendTheme(entry)
                appendEmuLinks(entry)
                entry["visible"] = True
            else:
                if(configuration["options"]["showAll"]):
                    appendTheme(entry)
                    entry["visible"] = True
                else:
                    appendTheme(entry)
                    entry["visible"] = False

        except Exception as ex:
            print("Error: " + str(ex))
    # check for old config
    if(upgrade):
        upgradeConfig()


def hasConfig(system):
    global configuration

    systems = system.split(",")
    found = False
    for (dirpath, dirnames, filenames) in os.walk(configuration["linkPath"]):
        for name in filenames:
            for system in systems:
                if(name.lower().startswith(system.strip().lower() + ".") or
                name.lower() == system.strip().lower()):
                    found = True
                    break

    return found


def createNativeItem(item):
    data = parseLink(item)

    entry = {}
    entry["name"] = data["title"]
    entry["cmd"] = data["exec"]
   
    entry["description"] = data["description"]

    if("params" in data):
        entry["params"] = data["params"]

    if("clock" in data):
        entry["overclock"] = data["clock"]

    entry["workingDir"] = os.path.abspath(
        os.path.join(data["exec"], os.pardir))

    preview = os.path.splitext(entry["cmd"])[0] + ".png"
    if(os.path.exists(preview)):
        entry["preview"] = preview

    if("selectordir" in data):
        entry["selector"] = True
        entry["selectionPath"] = data["selectordir"]

        if("selectorfilter" in data):
            filter = data["selectorfilter"].split(",")
            entry["fileFilter"] = list(set(filter))

    return entry


def appendEmuLinks(entry):
    global configuration
    systems = entry["system"].split(",")

    entry["emu"] = []  # clear emus
    entry["useSelection"] = False

    for (dirpath, dirnames, filenames) in os.walk(configuration["linkPath"]):
        for name in filenames:
            for system in systems:
                if(name.lower().startswith(system.strip().lower() + ".") or
                name.lower() == system.strip().lower()):
                    data = parseLink(dirpath + "/" + name)

                  

                    emuEntry = {}
                    emuEntry["name"] = data["title"]
                    emuEntry["cmd"] = data["exec"]

                    if("params" in data):
                        emuEntry["params"] = data["params"]

                    emuEntry["workingDir"] = os.path.abspath(
                        os.path.join(data["exec"], os.pardir))

                    entry["emu"].append(emuEntry)
                    if("selectorfilter" in data and "useFileFilter" in entry and entry["useFileFilter"]):
                        filter = data["selectorfilter"].split(",")
                        if("fileFilter" in entry):
                            filter.extend(entry["fileFilter"])
                        # make unique
                        entry["fileFilter"] = list(set(filter))

                    if("selectordir" in data):
                        entry["useSelection"] = True                   
                  


def parseLink(linkFile):
    f = open(linkFile, "r")
    data = {}
    file_as_list = f.readlines()

    for line in file_as_list:
        params = line.split("=", 1)
        if(len(params) == 2):
            data[params[0]] = params[1].rstrip()

    return data


def upgradeConfig():
    global configuration

    hasOldConfig = False

    if os.path.exists('config/config.json.old'):
        print("Importing old config")
        oldConf = json.load(open('config/config.json.old'))

        main = oldConf["mainMenu"]
        del oldConf["mainMenu"]
        del oldConf["version"]
        del oldConf["type"]

        configuration["options"].update(oldConf["options"])
        saveOptions(configuration["options"])

        #remove from old config
        del oldConf["options"]

        reloadConfiguration(False)


        for oldEntry in main:
            for newEntry in configuration["mainMenu"]:
                if(oldEntry["name"] == newEntry["name"]):
                    if "system" in oldEntry: del oldEntry["system"]

                    print("Updating " + newEntry["name"])
                   

                    newEntry.update(oldEntry)

                    hasOldConfig = True
        
        configuration.update(oldConf)
        os.remove('config/config.json.old')
    

    ##update themes
    itemlist = os.listdir("theme/themes")  
    for oldName in itemlist:
        if(oldName.endswith(".json.old")):
            print("found old theme " + oldName)
            newName = oldName.replace(".old", "")
            
            if(os.path.exists("theme/themes/" + newName)):
                try:
                    oldTheme = json.load(open("theme/themes/" + oldName))
                    newTheme = json.load(open("theme/themes/" + newName))
                    newTheme.update(oldTheme)
                    hasOldConfig = True

                    with open("theme/themes/" + newName, 'w') as fp:
                        json.dump(newTheme, fp, sort_keys=True, indent=4)

                    os.remove("theme/themes/" + oldName)

                except Exception as ex:
                    print("Error updating theme: " + str(ex))

            else:
                print("Keeping theme file " + newName)
                os.rename("theme/themes/" + oldName, "theme/themes/" + newName)
    if (hasOldConfig):            
        saveConfiguration()
        reloadConfiguration(False)


def saveOptions(options):
    allConfig = json.load(open('config/config.json'))
    allConfig["options"] = options

    with open('config/config.json', 'w') as fp:
        json.dump(allConfig, fp, sort_keys=True, indent=4)


def appendTheme(entry):
    global currentTheme

    themeName = configuration["options"]["themeName"]
    entryName = entry["name"]

    #print("tring to load theme for: " + "/" + themeName + "/" + entryName)

    if(entryName in currentTheme):
        entry.update(currentTheme[entryName])
    else:
        try:
          #  print("loaded default config for " + entryName)
            if("type" in entry):
                # if it hast type param, its a main menu entry

                themeConfig = json.load(open("theme/default.json"))
                entry.update(themeConfig)

        except Exception as ex:
            print(str(ex))


def saveTheme(entry):
    themeName = configuration["options"]["themeName"].lower()
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

        currentTheme[entryName] = theme

    except Exception as ex:
        print(str(ex))


def saveThemeFile():
    global configuration

    try:
        with open("theme/themes/" + configuration["options"]["themeName"] + ".json", 'w') as fp:
            json.dump(currentTheme, fp, sort_keys=True, indent=4)
    except Exception as ex:
        print("error storing theme file " + str(ex))


def loadLastPlayed():
    global configuration
    if("showLastPlayed" in configuration["options"] and configuration["options"]["showLastPlayed"]):
        print("loading last played games")
        try:
            lastPlayed = json.load(open("config/lastPlayed.json"))

            if(os.path.exists("config/lastPlayedData.json")):
                lastPlayedData = json.load(open("config/lastPlayedData.json"))
                lastPlayed["data"] = lastPlayedData["data"]
            else:
                newData = {}
                newData["data"] = []
                lastPlayed["data"] = []
                with open('config/lastPlayedData.json', 'w') as fp:
                    json.dump(newData, fp, sort_keys=True, indent=4)

            appendTheme(lastPlayed)

            configuration["mainMenu"].append(lastPlayed)
        except Exception as ex:
            print("Exception: " + str(ex))


def setResolution():
    global configuration

    if(isRS97()):
        configuration["screenWidth"] = 320
        configuration["screenHeight"] = 240

    #RS07 & K3P
    else:
        configuration["screenWidth"] = 480
        configuration["screenHeight"] = 272

    # windows platform or mac
    if(platform.processor() != ""):
        configuration["screenWidth"] = 320
        configuration["screenHeight"] = 240


def saveConfiguration():
    global configuration
    print("saving")
    try:
        subprocess.Popen(["sync"])
    except Exception:
        pass

    allConfig = copy.deepcopy(configuration)
    main = allConfig["mainMenu"]

    for index, item in enumerate(main):
        if(item["type"] == "native"):
            data = item["data"] if "data" in item else []
            item.pop('data', None)
            for dataIndex, dataItem in enumerate(data):
                saveTheme(dataItem)

        if(item["type"] != "lastPlayed"):
            if "source" in item:
                del item["source"]
            if "emu" in item:
                del item["emu"]
            if "fileFilter" in item:
                del item["fileFilter"]

            saveTheme(item)

        elif(item["type"] == "lastPlayed"):
            dataName = "config/" + "main" + "/lastPlayed.json"
            if("data" in item):
                del item["data"]
            saveTheme(item)

        item.pop('visible', None)

    with open('config/config.json', 'w') as fp:
        json.dump(allConfig, fp, sort_keys=True, indent=4)

    saveThemeFile()

    for l in listeners:
        l()

    print("Save finished")


def storeConfigPart(fileName, item):
    if not os.path.exists(os.path.dirname(fileName)):
        try:
            os.makedirs(os.path.dirname(fileName))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open(fileName, 'w') as fp:
        json.dump(item, fp, sort_keys=True, indent=4)


def getTheme():
    return theme


def toColor(input):
    return make_tuple(input)


def isRS97():
    return "type" in configuration and configuration["type"] == "RS97"


def addConfigChangedCallback(listener):
    listeners.append(listener)


def getPathData(path, data=None):
    if(data == None):
        data = configuration

    if path and data:
        args = path.split("/")
        element = args[0]
        if element:
            newPath = '/'.join(args[1:])
            value = data.get(element)
            return value if len(args) == 1 else getPathData(value, newPath)
