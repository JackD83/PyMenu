import json
lastUsed = None
lastSelectedLine = None
lastPath = None

def setLastUsedMain(json):
    global lastUsed
    lastUsed = json

def setLastSelectedLine(line):
    global lastSelectedLine
    lastSelectedLine = line

def setLastPath(path):
    global lastPath
    lastPath = path

def storeResume():
    try:
        resume = {}
        resume["main"]=lastUsed
        resume["line"]=lastSelectedLine
        resume["path"]=lastPath
        print("Storing resume file: " + str(lastUsed) + " line:"+ str(lastSelectedLine) + " lastPath" + str(lastPath))
        with open('/tmp/resume.json', 'w') as fp:
            json.dump(resume, fp,sort_keys=True, indent=4)
    except Exception as ex:
        pass