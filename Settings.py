# 
#  Settings.py
#  Class for working with settings
#  
#  Copyright 2009 Artem Yunusov. All rights reserved.
# 

import os
import datetime
from Foundation import *
from durus.file_storage import FileStorage
from durus.connection import Connection
from durus.persistent_dict import PersistentDict
        
def settingsFolder(appName):
    """Return settings folder"""
    paths = NSSearchPathForDirectoriesInDomains(NSApplicationSupportDirectory,NSUserDomainMask,True)
    basePath = (len(paths) > 0 and paths[0]) or NSTemporaryDirectory()
    fullPath = basePath.stringByAppendingPathComponent_(appName)
    if not os.path.exists(fullPath):
        os.mkdir(fullPath)
    return fullPath
      
class _Settings(object):
    """Settings singleton object"""
    
    _appName = "MacTimeLog"
    
    _defaultSettings = {
        "dateFormat": "%m-%d-%Y %H:%M",
        "timeFormat": "%H:%M",
        "logDateTimeFormat": "at %H:%M",
        "workEndTime": "06:00",
        "workDayLength": 3600*8,
        "timerInterval": 1,
        "showWorkTill": False,
        "showDateTime": False,
        "logPath": "%s/%s" % (settingsFolder(_appName), "log.txt"),
        "projectsDataPath": "%s/%s" % (settingsFolder(_appName), "projects"),
        "slackingDataPath": "%s/%s" % (settingsFolder(_appName), "slacking"),
        "logEditCommand": "open -a TextEdit \"%s\"",
        "projectSeparator": "::",
        "selectedProject": "Default",
        "startPlaceholder": "__start__",
        "showNotification": False,
        "notificationTime": 40,
        "notificationRepeatTime": 10,
        "soundOnNotification": False,
        "showHelpMessageOnStart": True
    }

    _globalSettings = {}

    def __init__(self):
        self._settingsFile = "%s/%s" % (settingsFolder(self._appName), "settings")
        self._conn = Connection(FileStorage(self._settingsFile))
        self._globalSettings = self._conn.get_root()

    def get(self, key):
        """Return setting value by key"""
        if key in self._globalSettings:
            return self._globalSettings[key]
        elif key in self._defaultSettings:
            return self._defaultSettings[key]
        else:
            pass

    def set(self, key, value):
        """Set setting value by key"""
        self._globalSettings[key] = value

    def sync(self):
        self._conn.commit()

    def __del__(self):
        self.sync()

Settings = _Settings()

