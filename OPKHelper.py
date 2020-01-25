
import mimetypes

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

def getFileExtensions(mime):
    if(not mimetypes.inited):
        mimetypes.init()
        initKnowMimetypes()

    types = mime.split(";")

    result = []

    for t in types:
        if(t):
            res = mimetypes.guess_all_extensions(t)
            #print("getting extensions for mime " + str(t) + " " + str(res))
            result.extend(res)

    if(len(result) == 0):
        result.append(".*")
        
    return result
         

def initKnowMimetypes():
    mimetypes.add_type("application/x-nes-rom", ".nes")
    mimetypes.add_type("application/x-snes-rom", ".sfc")
    mimetypes.add_type("application/x-gameboy-rom", ".gb")
    mimetypes.add_type("application/x-gbc-rom", ".gbc")
    mimetypes.add_type("application/x-genesis-rom" ,".md")
    mimetypes.add_type("application/x-megadrive-rom", ".md")
    mimetypes.add_type("application/x-genesis-rom" ,".32x")
    mimetypes.add_type("application/x-megadrive-rom", ".32x")

    mimetypes.add_type("application/x-sms-rom", ".sms")

    mimetypes.add_type("application/x-cd-image", ".bin")
    mimetypes.add_type("application/x-cd-image", ".chd")
    mimetypes.add_type("application/x-cd-image", ".cue")
    mimetypes.add_type("application/x-cd-image", ".pbp")


    mimetypes.add_type("application/x-ms-dos-executable", ".exe")
    mimetypes.add_type("application/x-ms-dos-executable", ".com")

    mimetypes.add_type("application/x-ms-dos-program", ".exe")
    mimetypes.add_type("application/x-ms-dos-program", ".com")

    mimetypes.add_type("application/x-ms-dos-batch", ".bat")


    mimetypes.add_type("application/x-gzip", ".zip")
    mimetypes.add_type("application/gzip", ".zip")

     