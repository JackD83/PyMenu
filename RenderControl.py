dirty = True
transition = True

def setDirty(d=True):  
    global dirty
    dirty = d

def isDirty():
    global dirty    
    return dirty

def setInTransition(d=True):   
    global transition
    transition = d

def isInTransition():
    global transition    
    return transition
