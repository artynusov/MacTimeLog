import os
from Foundation import *


def getApplicationDirectory(appName):
    """Return appliction directory path"""
    paths = NSSearchPathForDirectoriesInDomains(NSApplicationSupportDirectory,
            NSUserDomainMask, True)
    basePath = (len(paths) > 0 and paths[0]) or NSTemporaryDirectory()
    fullPath = basePath.stringByAppendingPathComponent_(appName)

    if not os.path.exists(fullPath):
        os.makedirs(fullPath)
    return fullPath


def initAppDirs(settings, app_name):
    """Assign application direcotries variables to settings object"""
    APP_DIR = getApplicationDirectory(app_name)
    settings.APP_DIR = APP_DIR
    settings.APP_NAME = app_name
    settings.LOG_PATH = '{0}/{1}'.format(APP_DIR, 'log.txt')
    settings.USER_PREFS_PATH = '{0}/{1}'.format(APP_DIR, 'user_prefs.ini')
    settings.PROJECTS_DATA_PATH = '{0}/{1}'.format(APP_DIR, 'projects')
    settings.SLACKING_DATA_PATH = '{0}/{1}'.format(APP_DIR, 'slacking')