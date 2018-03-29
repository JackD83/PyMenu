dirty = True
transition = True

def setDirty(d=True):  
    global dirty
    dirty = d

def isDirty():
    global dirty    
    return dirty
