import subprocess, ResumeHandler
import platform,copy, json, Common
import sys, os, stat, Overclock

def runEmu(config, rom):
    ResumeHandler.storeResume()
    Common.addToCustomList(config, rom, "lastPlayedData")

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
    Common.addToCustomList(config, None, "lastPlayedData")
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



    
