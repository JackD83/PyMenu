import subprocess, ResumeHandler
import platform,copy, json, Common
import sys, os, stat, Overclock

def runEmu(config, rom):
    ResumeHandler.storeResume()
    addToLastPlayed(config, rom)

    name =  config["name"]
    workdir = config["workingDir"] if "workingDir" in config else None
    cmd =  config["cmd"] if "workingDir" in config else None


    if(cmd == None or not os.path.isfile(cmd)):
        print("cmd needs to be set to an existing executable")       
        return
    
    print("Platform is: '" + platform.processor() + "'")
    if(workdir == None and not cmd == None):    
        workdir = os.path.abspath(os.path.join(cmd, os.pardir))   

    
    if(platform.processor() == ""):
        runEmuMIPS(name, cmd, workdir, config, rom)
    else:
        runEmuHost(name, cmd, workdir, config, rom)

def runEmuMIPS(name, cmd, workdir, config, rom):
    name =  config["name"]
    cmd =  config["cmd"] if "cmd" in config else None
    workdir = config["workingDir"] if "workingDir" in config else None 
    overclock = config["overclock"] if "overclock" in config else None
    params = config["params"] if "params" in config else None

    if(workdir == None and not cmd == None):    
        workdir = os.path.abspath(os.path.join(cmd, os.pardir))

    if(overclock != None):
        try:
           Overclock.setClock(overclock)
        except Exception as ex:
            pass

    fileName = "run"   
    file = open("/tmp/" + fileName,"w")
    file.write("#!/bin/sh\n")
    file.write("export HOME=/home/retrofw\n")

   
    file.write("cd \"" + workdir + "\"\n")

    if(params != None):
        file.write(cmd + " " + params.replace("$f","\""+  rom + "\"") + "\n")
    else:
        file.write(cmd + " \"" + rom + "\"\n")     

    file.close() 
    
    st = os.stat('/tmp/' + fileName)
    os.chmod('/tmp/' + fileName, st.st_mode | stat.S_IEXEC)
   
    sys.exit()
   

def runEmuHost(name, cmd, workdir, config, rom):  
    print("run emu " + cmd + " " + name + " with file " + rom + " cwd " +workdir)
    try:
        subprocess.Popen([cmd, rom ], cwd=workdir)
    except Exception as ex:
        print(str(ex))
    

def runNative(config):
    ResumeHandler.storeResume()
    addToLastPlayed(config, None)
    cmd =  config["cmd"] if "cmd" in config else None
  
    if(cmd == None or not os.path.isfile(cmd)):
        print("cmd needs to be set to an existing executable")      
        return
    
    print("Platform is: " + platform.processor())
        
    if(platform.processor() == ""):
        runNativeMIPS(cmd, config)
    else:
        runNativeHost(cmd, config)

def runNativeMIPS(cmd, config):  
    cmd =  config["cmd"] if "cmd" in config else None
    screen = config["screen"] if "screen" in config else None  
    overclock = config["overclock"] if "overclock" in config else None
    selection = config["selection"] if "selection" in config else ""
    params = config["params"] if "params" in config else None

    if(overclock != None):
        try:
            Overclock.setClock(overclock)
        except Exception as ex:
            pass


    fileName = "run"

    file = open("/tmp/" + fileName,"w")
    file.write("#!/bin/sh\n")
    file.write("export HOME=/home/retrofw\n")  

    parent = os.path.abspath(os.path.join(cmd, os.pardir))
    file.write("cd \"" + parent + "\"\n")

    if(params != None):
        file.write(cmd + " " + params.replace("$f","\""+  selection + "\"") + "\n")
    else:
        file.write("\"" + cmd  + "\" \"" + selection + "\"\n")     

  

    file.close() 
    st = os.stat('/tmp/' + fileName)
    os.chmod('/tmp/' + fileName, st.st_mode | stat.S_IEXEC)
   
    sys.exit()

    

def runNativeHost(cmd, config):
    selection = overclock = config["selection"] if "selection" in config else ""   
    try:
        subprocess.Popen([cmd, selection])
    except Exception as ex:
        print(str(ex))

def addToLastPlayed(config, rom):
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
            data["name"] = Common.getGameName(filename_w_ext)
            data["gameListName"] = data["name"]
           
        
        

        data["rom"] = rom
        data["type"] = "emulator"

        if(not "preview" in data):
            data["preview"] = ""

        if("previews" in config and not config["previews"] == None):
             data["preview"] = str(config["previews"]) + "/" + str(filename) + ".png"

        

    else:
        data["type"] = "native"   


    try:
        lastPlayed = json.load(open("config/lastPlayedData.json"))
       

        last = wasLastPlayed(lastPlayed, data)
        if(   last != None ):            
            lastPlayed["data"].remove(last)          


        lastPlayed["data"].insert(0, data)
        lastPlayed["data"] = lastPlayed["data"][0:20]

        with open('config/lastPlayedData.json', 'w') as fp: 
            json.dump(lastPlayed, fp,sort_keys=True, indent=4)

        
    except Exception as ex:
        print("Exception " + str(ex))        

def wasLastPlayed(lastPlayed, data):
    for last in lastPlayed["data"]:
        if( (data["type"] == "emulator" and last["type"] == "emulator" and last["rom"] == data["rom"]) or (data["type"] == "native" and last["type"] == "native" and last["cmd"] == data["cmd"]) ):   
     
            return last
          
    return None


    
