
def initGlobalVar():
    """initialize variable"""
    global GLOBALS_DICT
    GLOBALS_DICT = {}


def setVar(name, value):
    """set variable"""
    try:
        GLOBALS_DICT[name] = value
        return True
    except KeyError:
        return False


def getVar(name):
    """get variable"""
    try:
        return GLOBALS_DICT[name]
    except KeyError:
        return "Not Found"
