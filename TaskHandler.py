import uuid, Common

animations = {}
preiodic = {}
counter = 0


def addPeriodicTask(time, callback):
    id = uuid.uuid4()

    task = {}
    task["start"] = counter
    task["val"] = Common.FPS / 1000 * time
    task["callback"] = callback

    preiodic[id] = task

    return id

def removePeriodicTask(id):
     del preiodic[id]

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

        if(animations[anim]["current"] >= animations[anim]["target"]):
            animations[anim]["callback"](animations[anim]["target"], True)
            toDelete.append(anim)
        else:
            animations[anim]["callback"](animations[anim]["current"], False)    

    for anim in toDelete:
        del animations[anim]

    for task in preiodic:
        time = counter - preiodic[task]["start"]
        if( time != 0 and preiodic[task]["val"] != 0 and time % preiodic[task]["val"] == 0):          
            preiodic[task]["callback"]()

