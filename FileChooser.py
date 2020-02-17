# -*- coding: utf-8 -*-
import RenderObject, Configuration, AbstractList
import os, Keys, RenderControl, Common
import pygame, sys, ResumeHandler, ntpath
from threading import Thread
from operator import itemgetter
from time import sleep
import SelectionMenu
import json
import copy

try:        
    import scandir
    print("using native scandir")     
except Exception as ex:
    sys.path.insert(0, "scandir")
    import scandir
    print("using custom scandir")    


class FileChooser(AbstractList.AbstractList):
   
    folderIcon = Common.loadImage( "theme/folder.png")
    reset = None
    
    overlay = None
   
    currentSelection = ""
    previewTmp = None

    def render(self, screen):
        AbstractList.AbstractList.render(self, screen)      

        if(self.overlay != None):           
            self.overlay.render(screen)

    def renderText(self, entry):
        text = self.entryFont.render(self.filterName(entry["name"]), True, self.textColor)
        entry["text"] = text
        return text
 
    def renderEntry(self, screen, index, xOffset, yOffset):
        text = self.entryList[index]["text"]
        if(text== None):
            text = self.renderText(self.entryList[index])
       

        yTextOffset = (self.listEntryHeight -  text.get_height()) / 2
              
        if(self.entryList[index]["isFolder"]):
            screen.blit(text, (self.listEntryHeight + 4 + xOffset, yOffset + yTextOffset))
            screen.blit(self.folderIcon, (self.xFolderOffset+ xOffset, yOffset +  self.yFolderOffset) )
        else:
            screen.blit(text, (2 + xOffset, yOffset + yTextOffset))
    

    def loadFolder(self, folder):
       
        if(folder["name"] == ".."):
           self.moveFolderUp()          
        else:
            self.currentPath += "/" + folder["name"]
            self.currentWrap = 0
            self.currentIndex = 0
            self.initList()
        
        
    
    def setOverlay(self, overlay):
        self.overlay = overlay
           
    def moveFolderUp(self):
        self.reset = None
        self.reset = os.path.basename(self.currentPath)
        self.currentPath = os.path.abspath(os.path.join(self.currentPath, os.pardir))
        self.currentWrap = 0
        self.currentIndex = 0
        self.initList()

        
    
    def setFooter(self, footer):
        AbstractList.AbstractList.setFooter(self, footer)
        
        
    def onSelect(self, key=Keys.DINGOO_BUTTON_A):
        if(len(self.entryList) == 0):
            self.callback(None)
            return

        if(self.entryList[self.currentIndex]["isFolder"]):
            self.loadFolder(self.entryList[self.currentIndex])
        else:
            ResumeHandler.setLastSelectedLine(self.currentIndex)
            ResumeHandler.setLastPath(os.path.normpath(self.currentPath + "/"))
            self.callback(os.path.normpath(self.currentPath + "/" + self.entryList[self.currentIndex]["name"]), key)
    
    def onExit(self):
        if(self.selectFolder):
            self.callback(os.path.normpath(self.initialPath))
        else:
            self.callback(None)
    
    def onChange(self):
        if(len(self.entryList) == 0):
            self.currentSelection = None
            self.previewPath = None
            return

        self.currentSelection = self.currentPath + "/" + self.entryList[self.currentIndex]["name"]
        self.currentSelection =  os.path.normpath(self.currentSelection)
        self.previewPath = None

        if("directPreview" in self.options and self.options["directPreview"] and self.isImage()):
             self.previewPath = self.currentSelection           
             return
        if("previews" in self.options and self.options["previews"] != None and os.path.exists(self.options["previews"]) and self.currentSelection != None):
            self.previewPath = self.options["previews"] + "/" + os.path.splitext(os.path.basename(self.currentSelection))[0] + ".png"
        
            if(not self.previewPath != None and not os.path.exists(self.previewPath)):
                self.previewPath = None
       


    def handleEvents(self, events):     
        if(self.overlay != None):
            self.overlay.handleEvents(events)
            return

        for event in events:    
            if event.type == pygame.KEYDOWN:                        
                if event.key == Keys.DINGOO_BUTTON_LEFT:
                    if (( ("limitSelection" in self.options 
                        and self.options["limitSelection"] )
                        and os.path.normpath(self.options["selectionPath"]) == os.path.normpath(self.currentPath)  )
                        or ("hideFolders" in self.options and self.options["hideFolders"]) ):
                        pass
                    else:
                        self.moveFolderUp()
                        RenderControl.setDirty()
            if event.type == pygame.KEYUP:         
                if event.key == Keys.DINGOO_BUTTON_START:
                    if(self.selectFolder):
                        if(self.entryList[self.currentIndex]["isFolder"] and self.entryList[self.currentIndex]["name"] != ".."):
                            self.callback(self.currentPath + "/" + self.entryList[self.currentIndex]["name"])
                            
                        else:
                            self.callback(self.currentPath)
                            
                        RenderControl.setDirty()
                        return
                    else:
                        self.onSelect(Keys.DINGOO_BUTTON_START)
                elif (event.key == Keys.DINGOO_BUTTON_SELECT and "showFavourites" in self.config["options"] 
                and self.config["options"]["showFavourites"] and not self.entryList[self.currentIndex]["isFolder"]):
                   self.showFavouriteOverlay()
               

        AbstractList.AbstractList.handleEvents(self, events)

    def showFavouriteOverlay(self):
        selected = os.path.normpath(self.currentPath + "/" + self.entryList[self.currentIndex]["name"])
        isFav = Common.isFavourite(self.options["entry"],selected)

        if(isFav):
            opt = ["Remove from favourites"]
        else:
            opt = ["Add to favourites"]
        
        overlay = SelectionMenu.SelectionMenu(self.screen,opt, self.favouriteCallback, width=180)
        self.setOverlay(overlay)
    
     

    def favouriteCallback(self, index, res):
       
        self.setOverlay(None)
        selected = os.path.normpath(self.currentPath + "/" + self.entryList[self.currentIndex]["name"])

        if(res == "Add to favourites"):
            if("emu" in self.options["entry"]):
                emus = []
                for e in self.options["entry"]["emu"]:
                    emus.append(e["name"])


                if(len(emus) == 1):
                    self.emuSelectionCallback(0, emus[0])

                elif(len(emus) > 0):
                    overlay = SelectionMenu.SelectionMenu(self.screen, emus, self.emuSelectionCallback)
                    self.setOverlay(overlay)
                    RenderControl.setDirty()

           
        elif(res == "Remove from favourites"):
            Common.removeFavourite(self.options["entry"],selected )



      

    def emuSelectionCallback(self, index, selection):
        self.overlay = None

        if(index != -1):
            selected = os.path.normpath(self.currentPath + "/" + self.entryList[self.currentIndex]["name"])

            if(selected != None):
                data = copy.deepcopy(self.options["entry"])
                data["cmd"] = data["emu"][index]["cmd"]
                data["workingDir"] = data["emu"][index]["workingDir"]
                if "params" in data["emu"][index]: data["params"] = data["emu"][index]["params"]
            
                Common.addFavourite(data,selected )
     
            
       
   
    def initList(self):
        self.listReady = False  
        thread = Thread(target = self.initListAsync, args = ())
        thread.start()
        sleep(0.05) #allows to skip the drawing of waiting symbol if folder is loaded in 5ms
       

    def initListAsync(self):
        if("useGamelist" in self.options and self.options["useGamelist"] == True):
            Common.loadGameList()

        selectFileAfterLoad = None
        if(os.path.isfile(self.initialPath)):
            selectFileAfterLoad = ntpath.basename(self.initialPath)
            

        if(os.path.isdir(self.currentPath) and os.path.exists(self.currentPath)):
            self.entryList = []

            folderList = []
            fileList = []

             ##append ..
            if(( ("limitSelection" in self.options 
                and self.options["limitSelection"] )
                and os.path.normpath(self.options["selectionPath"]) == os.path.normpath(self.currentPath))
                or ("hideFolders" in self.options and self.options["hideFolders"]) ):
                pass
                ##dont add ..
            else:
                entry = {}
                entry["name"] = ".."
                entry["isFolder"] = True
                entry["text"] = self.entryFont.render("..", True, self.textColor)
                self.entryList.append(entry)

            scan = scandir.scandir(os.path.normpath(self.currentPath))
        
            try:
                hideFolders  = self.options["hideFolders"] if "hideFolders" in self.options else False

                for f in scan:  
                           
                    if(f.is_dir() and not hideFolders ):
                        entry = {}
                        entry["name"] = f.name
                        entry["isFolder"] = True
                        entry["text"] = None
                        folderList.append(entry)
                    elif ( not self.selectFolder and self.filterFile(f.name)):
                        entry = {}
                        entry["name"] = f.name
                        entry["isFolder"] = False
                        entry["text"] = None
                        fileList.append(entry)
                
                Common.quick_sort(folderList)
                Common.quick_sort(fileList)

                self.entryList = self.entryList + folderList + fileList
                
            except Exception as ex:
                pass    

        if(not self.reset == None):
            for entry in self.entryList:
                if(entry["name"] == self.reset):
                    self.setSelection(self.entryList.index(entry))
        elif(selectFileAfterLoad != None):
            for entry in self.entryList:
                if(entry["name"] == selectFileAfterLoad):
                    self.setSelection(self.entryList.index(entry))

        elif(self.res != None and self.res["line"] != None):           
            self.setInitialSelection(self.res["line"])
            self.res = None
        else:
            self.setSelection(0)
        

        self.listReady = True
        self.onChange()
        AbstractList.AbstractList.updatePreview(self)
        
        RenderControl.setDirty()

        


    def getExistingParent(self, path):
        if(path == "/" or path == "" or path == "."):
            return "/"

        parent = os.path.abspath(os.path.join(path, os.pardir))
        if(parent == path):
            return path

        if(os.path.exists(parent)):
            return parent
        else:
            return self.getExistingParent(parent)

    def isImage(self):
        if(self.currentSelection.lower().endswith("png") or 
            self.currentSelection.lower().endswith("jpg") ):
            return True

        
    def filterName(self, filename):
        if("useGamelist" in self.options and self.options["useGamelist"] == True):
            return Common.getGameName(filename)

        if(not "fileFilter" in self.options or "useFileFilter" not in self.options
            or not self.options["useFileFilter"]):
        
            return filename

        return os.path.splitext(filename)[0]
        
        

    def filterFile(self, file):
        if(not "fileFilter" in self.options or ("useFileFilter" in self.options
            and not self.options["useFileFilter"])):
            return True #allow all files

        #check if all files are allowed using filter, will allow filering of all file extensions
        if(".*" in self.options["fileFilter"]):
            return True

        filename, file_extension = os.path.splitext(file)
        if(file_extension == ""):
            return False

        if any(file_extension in s for s in self.options["fileFilter"]):
            return True

        return False
    
    def setInitialSelection(self, index):
        self.setSelection(index)
        self.onChange()            
        self.preview_final = self.previewPath            
        RenderControl.setDirty()
    
  

    def __init__(self, screen, titel, initialPath, selectFolder, options, callback):        
        AbstractList.AbstractList.__init__(self,screen, titel, options)

        print("Opening selection with options: " + str(options))
      
        if(initialPath == None or initialPath == "/"):
            initialPath = "/"

        self.getExistingParent(initialPath)

        if(os.path.exists(initialPath) and not os.path.isfile(initialPath)):          
            self.currentPath = initialPath
        else:
            self.currentPath = self.getExistingParent(initialPath)

        if("directPreview" in self.options and self.options["directPreview"]):
            self.previewEnabled = True

        if("previews" in self.options and self.options["previews"] != None and os.path.exists(self.options["previews"]) ):
            self.previewEnabled = True
        
           
        self.currentSelection = initialPath
        self.initialPath = initialPath       
        self.selectFolder = selectFolder  
        self.callback = callback

        #tint folder icon in text color
        self.folderIcon =  self.folderIcon.convert_alpha().copy()
        self.folderIcon.fill(self.textColor, None, pygame.BLEND_RGBA_MULT)   

        self.yFolderOffset = (self.listEntryHeight - self.folderIcon.get_height()) / 2
        self.xFolderOffset = (self.listEntryHeight - self.folderIcon.get_width()) / 2 + 2

        self.yFileOffset =  0
        
        self.res = ResumeHandler.getResumeFile()
        if(self.res != None and self.res["path"] != None):
            self.currentSelection = self.res["path"]
            self.currentPath = self.res["path"]
            self.initialPath = self.res["path"]

        self.initList()
     

        if(initialPath == None or initialPath == "/"):
            self.moveFolderUp()

       
        self.onChange()

        
        
      
