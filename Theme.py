from ast import literal_eval as make_tuple
import Configuration
import Common


def getColor(path, default):
    try:
        theme = Configuration.getTheme()
        color = Common.pathGet(theme, path)
        res =  make_tuple(color)
        return res

    except Exception as ex:
        return default

def getValue(path, default):
    try:

        theme = Configuration.getTheme()
        value = Common.pathGet(theme, path)
        return value

    except Exception as ex:
        return default

def getConfigOptions():
    opt =  {}
    opt["backgroundColor"] = getColor("settings/backgroundColor", (0,0,0))
    opt["textColor"] = getColor("settings/fontColor", (255,255,255))
    opt["sideColor"] = getColor("settings/sideCOlor", (57,58,59))

    opt["headerColor"] = getColor("settings/header/color",(57,58,59))
    opt["headerFontColor"] = getColor("settings/header/fontColor", (255,255,255))
    opt["descriptionFontColor"] = getColor("settings/header/descriptionFontColor", (255,255,255))
    opt["selectionColor"] = getColor("settings/selectionColor", (255,255,255,128))
    opt["footerColor"]  = getColor("settings/footer/color", (57,58,59))
    opt["footerFontColor"]  = getColor("settings/footer/fontColor", (255,255,255))
    opt["scrollbarColor"]  = getColor("settings/scrollbarColor", (105,105,105))

    return opt

def getSelectionOptions():
    options = {}
    options["backgroundColor"] = getColor("selection/backgroundColor", (255,255,255, 200))
    options["textColor"] = getColor("selection/fontColor", (0,0,0))
    options["sideColor"] = getColor("selection/sideColor", (57,58,59))
    options["headerColor"] = getColor("selection/header/color",(57,58,59))
    options["headerFontColor"] = getColor("selection/header/fontColor", (255,255,255))
    options["descriptionFontColor"] = getColor("selection/header/descriptionFontColor", (255,255,255))
    options["selectionColor"] = getColor("selection/selectionColor", (55,55,55,128))
    options["footerColor"] =  getColor("selection/footer/color", (57,58,59))
    options["footerFontColor"] = getColor("selection/footer/fontColor", (255,255,255))
    options["scrollbarColor"]  = getColor("selection/scrollbarColor", (105,105,105))

    return options

