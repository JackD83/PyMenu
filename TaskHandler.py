import uuid, Common, math

animations = {}
periodic = {}
counter = 0


def addPeriodicTask(time, callback, delay=0):
    id = uuid.uuid4()

    task = {}
    task["delay"] = counter + (Common.FPS / 1000 * delay)
    task["start"] = counter
    task["val"] = Common.FPS / 1000 * time
    task["callback"] = callback

    periodic[id] = task

    return id

def removePeriodicTask(id):
     if(id in periodic):
        del periodic[id]
    
def stopAnimation(id):
    if(id in animations):
        print("Animation stopped")
        del animations[id]

def addAnimation(start, target, duration, callback, delay = 0):
    id = uuid.uuid4()
    anim = {}
    anim["delay"] = counter + (Common.FPS / 1000 * delay)
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
        if(counter >= animations[anim]["delay"]):
            animations[anim]["current"] = animations[anim]["current"] + animations[anim]["speed"]

            finished = False
            if(animations[anim]["target"] > animations[anim]["start"]):
                finished = animations[anim]["current"] >= animations[anim]["target"]
            else:
                finished = animations[anim]["current"] <= animations[anim]["target"]
            
        
            if(finished):
                animations[anim]["callback"](animations[anim]["start"], animations[anim]["target"], animations[anim]["current"], True)
                toDelete.append(anim)
            else:
                animations[anim]["callback"](animations[anim]["start"], animations[anim]["target"], animations[anim]["current"], False)    

    for anim in toDelete:
        del animations[anim]

    for task in periodic:
        if(counter >= periodic[task]["delay"]):
            time = counter - periodic[task]["start"]
            if( time != 0 and periodic[task]["val"] != 0 and time % periodic[task]["val"] == 0):          
                periodic[task]["callback"]()

