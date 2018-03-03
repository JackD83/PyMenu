import json
from ast import literal_eval as make_tuple
from pprint import pprint

configuration = json.load(open('config/config.json'))
theme = json.load(open('theme/theme.json'))

def getConfiguration():
    return configuration

def getTheme():
    return theme

def toColor(input):
    return make_tuple(input)

