import json
from ast import literal_eval as make_tuple
from pprint import pprint

configuration = json.load(open('config.json'))
theme = json.load(open('theme.json'))

def getConfiguration():
    return configuration

def getTheme():
    return theme

def toColor(input):
    return make_tuple(input)

