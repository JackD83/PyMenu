import uuid, Common, math

animations = {}
periodic = {}
counter = 0


def addPeriodicTask(time, callback):
    id = uuid.uuid4()

    task = {}
    task["start"] = counter
    task["val"] = Common.FPS / 1000 * time
    task["callback"] = callback

    periodic[id] = task

    return id

def removePeriodicTask(id):
     del periodic[id]

def addAnimation(start, target, duration, callback):
    id = uuid.uuid4()
    anim = {}
    anim["start"] = start
    anim["target"] = target
    anim["speed"] =  (target- start) / (Common.FPS / 1000 * duration)
    anim["current"] = start
    anim["callback"] = callback
    
    animations[id] = anim 

    return id

def updateTasks():
    global counter
    counter = counter + 1

    toDelete = []
    for anim in animations:
        animations[anim]["current"] = animations[anim]["current"] + animations[anim]["speed"]

        if(math.fabs(animations[anim]["current"]) >= math.fabs(animations[anim]["target"])):
            animations[anim]["callback"](animations[anim]["start"], animations[anim]["target"], animations[anim]["current"], True)
            toDelete.append(anim)
        else:
            animations[anim]["callback"](animations[anim]["start"], animations[anim]["target"], animations[anim]["current"], False)    

    for anim in toDelete:
        del animations[anim]

    for task in periodic:
        time = counter - periodic[task]["start"]
        if( time != 0 and periodic[task]["val"] != 0 and time % periodic[task]["val"] == 0):          
            periodic[task]["callback"]()

