import subprocess
import platform
import sys, os

def runEmu(config, rom):
    name =  config["name"]
    workdir = config["workingDir"] if "workingDir" in config else None
    cmd =  config["cmd"] if "workingDir" in config else None

    if(cmd == None or not os.path.isfile(cmd)):
        print("cmd needs to be set to an existing executable")
        #return
    
    print("Platform is: " + platform.processor())
    if(workdir == None and not cmd == None):    
        workdir = os.path.abspath(os.path.join(cmd, os.pardir))   

 
    
    if( "MIPS" in platform.processor()):
        runEmuMIPS(name, cmd, workdir, config, rom)
    else:
        runEmuHost(name, cmd, workdir, config, rom)

def runEmuMIPS(name, cmd, workdir, config, rom):
    name =  config["name"]
    workdir = config["workingDir"] if "workingDir" in config else None
    cmd =  config["cmd"] if "cmd" in config else None
    screen = config["screen"] if "screen" in config else None
    legacy = config["legacy"] if "legacy" in config else None


    if(legacy != "True"):
        file = open("/tmp/run","w")
        file.write("#!/bin/sh\n")

        if(screen != None):
            if(screen == "fullscreen"):
                file.write("echo 2 > /proc/jz/lcd_a320\n")
            if(screen == "center"):
                file.write("echo 1 > /proc/jz/lcd_a320\n")

        file.write("cd " + workdir + "\n")
        file.write(cmd + " " + rom + "\n")

        if(screen != None and screen != "default"):
            file.write("echo 0 > /proc/jz/lcd_a320\n")
        file.close() 
    else:
        print("Legacy mode not supported yet")

def runEmuHost(name, cmd, workdir, config, rom):  
    print("run emu " + cmd + " " + name + " with file " + rom + " cwd " +workdir)
    subprocess.Popen([cmd, rom ], cwd=workdir)

def runNative(config):
    print(config)
    cmd =  config["cmd"] if "cmd" in config else None

    if(cmd == None or not os.path.isfile(cmd)):
        print("cmd needs to be set to an existing executable")
        #return
    
    print("Platform is: " + platform.processor())
        
    if( "MIPS" in platform.processor()):
        runNativeMIPS(cmd, config)
    else:
        runNativeHost(cmd, config)

def runNativeMIPS(cmd, config):  
    cmd =  config["cmd"] if "cmd" in config else None
    screen = config["screen"] if "screen" in config else None
    legacy = config["legacy"] if "legacy" in config else None

    if(legacy != "True"):
        file = open("/tmp/run","w")
        file.write("#!/bin/sh\n")

        if(screen != None):
            if(screen == "fullscreen"):
                file.write("echo 2 > /proc/jz/lcd_a320\n")
            if(screen == "center"):
                file.write("echo 1 > /proc/jz/lcd_a320\n")
   
        file.write(cmd + "\n")

        if(screen != None and screen != "default"):
            file.write("echo 0 > /proc/jz/lcd_a320\n")
        file.close() 
    else:
        print("Legacy mode not supported yet")

def runNativeHost(cmd, config):
    subprocess.Popen([cmd])