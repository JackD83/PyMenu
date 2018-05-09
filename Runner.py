import subprocess
import platform
import sys, os, stat

def runEmu(config, rom):
    name =  config["name"]
    workdir = config["workingDir"] if "workingDir" in config else None
    cmd =  config["cmd"] if "workingDir" in config else None

    if(cmd == None or not os.path.isfile(cmd)):
        print("cmd needs to be set to an existing executable")
        return
    
    print("Platform is: " + platform.processor())
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
    screen = config["screen"] if "screen" in config else None
    legacy = config["legacy"] if "legacy" in config else None
    overclock = config["overclock"] if "overclock" in config else None

    if(workdir == None and not cmd == None):    
        workdir = os.path.abspath(os.path.join(cmd, os.pardir))   

    if(overclock != None):
        try:
            subprocess.Popen(["overclock.dge", overclock])
        except Exception as ex:
            pass

    fileName = "run"
    if(legacy == "True"):
        fileName ="legacyRun"

    file = open("/tmp/" + fileName,"w")
    file.write("#!/bin/sh\n")

    if(legacy == "True"):
        file.write("export HOME=/mnt/ext_sd/home/\n")

    if(screen != None):
        if(screen == "fullscreen"):
            file.write("echo 2 > /proc/jz/lcd_a320\n")
        if(screen == "center"):
            file.write("echo 1 > /proc/jz/lcd_a320\n")

    file.write("cd \"" + workdir + "\"\n")
    file.write(cmd + " \"" + rom + "\"\n")

    if(screen != None and screen != "default"):
        file.write("echo 0 > /proc/jz/lcd_a320\n")

    file.close() 
    
    st = os.stat('/tmp/' + fileName)
    os.chmod('/tmp/' + fileName, st.st_mode | stat.S_IEXEC)


    if(legacy == "True"):
        file = open("/tmp/run","w")
        file.write("#!/bin/sh\n")
        file.write("mount --bind /mnt/ext_sd/ /opt/legacy/mnt/ext_sd/\n")
        file.write("mount --bind /mnt/int_sd/ /opt/legacy/mnt/int_sd/\n")       
        file.write("chroot /opt/legacy /tmp/legacyRun\n")
        file.close()
        st = os.stat('/tmp/run')
        os.chmod('/tmp/run', st.st_mode | stat.S_IEXEC)

    sys.exit()
   

def runEmuHost(name, cmd, workdir, config, rom):  
    print("run emu " + cmd + " " + name + " with file " + rom + " cwd " +workdir)
    try:
        subprocess.Popen([cmd, rom ], cwd=workdir)
    except Exception as ex:
        print(str(ex))
    

def runNative(config):
    print(config)
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
    legacy = config["legacy"] if "legacy" in config else None
    overclock = config["overclock"] if "overclock" in config else None

    if(overclock != None):
        try:
            subprocess.Popen(["overclock.dge", overclock])
        except Exception as ex:
            pass


    fileName = "run"
    if(legacy == "True"):
        fileName ="legacyRun"

    file = open("/tmp/" + fileName,"w")
    file.write("#!/bin/sh\n")

    if(legacy == "True"):
        file.write("export HOME=/mnt/ext_sd/home/\n")

    if(screen != None):
        if(screen == "fullscreen"):
            file.write("echo 2 > /proc/jz/lcd_a320\n")
        if(screen == "center"):
            file.write("echo 1 > /proc/jz/lcd_a320\n")

    parent = os.path.abspath(os.path.join(cmd, os.pardir))
    file.write("cd \"" + parent + "\"\n")
    file.write("\"" + cmd + "\"\n")

    if(screen != None and screen != "default"):
        file.write("echo 0 > /proc/jz/lcd_a320\n")

    file.close() 
    st = os.stat('/tmp/' + fileName)
    os.chmod('/tmp/' + fileName, st.st_mode | stat.S_IEXEC)

    if(legacy == "True"):
        file = open("/tmp/run","w")
        file.write("#!/bin/sh\n")
        file.write("mount --bind /mnt/ext_sd/ /opt/legacy/mnt/ext_sd/\n")
        file.write("mount --bind /mnt/int_sd/ /opt/legacy/mnt/int_sd/\n")    
        file.write("chroot /opt/legacy /tmp/legacyRun\n")
        file.close()
        st = os.stat('/tmp/run')
        os.chmod('/tmp/run', st.st_mode | stat.S_IEXEC)
    sys.exit()

    

def runNativeHost(cmd, config):
    try:
        subprocess.Popen([cmd])
    except Exception as ex:
        print(str(ex))
   