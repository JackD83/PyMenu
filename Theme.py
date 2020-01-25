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


