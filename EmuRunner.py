import subprocess
import sys

def runEmu(config, rom):
    print("run emu " + config["cmd"] + " " + config["name"] + " with file " + rom + " cwd " + config["workingDir"])
    subprocess.Popen([config["cmd"], rom ], cwd=config["workingDir"])
    sys.exit(0)

