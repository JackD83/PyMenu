
hasLibOPK = False
try:
    import OPK
    hasLibOPK = True
except Exception as ex:
    print("libopk is not available")


def getMetadataForExec(opk, ex):
    if(not hasLibOPK):
        return None

    meta = OPK.read_metadata(opk)       

    for desktop in meta:
        try:
            name = desktop
            exe =  meta[desktop]["Desktop Entry"]["Exec"].lower()

            if(ex == exe):
                print("Found meta from " + opk + " " + ex + " " + name)
                return name

         
        except Exception as ex:
            print("Could not load OPK " + str(ex))
    
    return None