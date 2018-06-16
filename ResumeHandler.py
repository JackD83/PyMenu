import json, os
lastUsed = None
lastSelectedLine = None
lastPath = None
mainIndex = None

def setLastUsedMain(json, index):
    global lastUsed
    global mainIndex
    lastUsed = json
    mainIndex = index

def clearResume():
    try:
        os.remove("/tmp/resume.json")
    except Exception as ex:
        return None

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
        resume["mainIndex"]= mainIndex
        resume["line"]=lastSelectedLine
        resume["path"]=lastPath
        print("Storing resume file: " + str(lastUsed) + " line:"+ str(lastSelectedLine) + " lastPath" + str(lastPath))
        with open('/tmp/resume.json', 'w') as fp:
            json.dump(resume, fp,sort_keys=True, indent=4)
    except Exception as ex:
        pass

def getResumeFile():
    try:
        res = json.load(open('/tmp/resume.json'))
        return res      
    except Exception as ex:
        return None