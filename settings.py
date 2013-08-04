#
#  settings.py
#  Class for working with settings
#
#  Copyright 2009 Artem Yunusov. All rights reserved.
#

import os
import logging

from Foundation import *

from durus.file_storage import FileStorage
from durus.connection import Connection


def getSettingsFolder(appName):
    """Return settings folder"""
    paths = NSSearchPathForDirectoriesInDomains(NSApplicationSupportDirectory,
            NSUserDomainMask, True)
    basePath = (len(paths) > 0 and paths[0]) or NSTemporaryDirectory()
    fullPath = basePath.stringByAppendingPathComponent_(appName)

    if not os.path.exists(fullPath):
        os.makedirs(fullPath)

    return fullPath


class _Settings(object):
    """Settings singleton object"""

    _appName = "MacTimeLog"

    _defaultSettings = dict(

        dateFormat="%m-%d-%Y %H:%M",

        timeFormat="%H:%M",

        logDateTimeFormat="at %H:%M",

        workEndTime="06:00",

        workDayLength=3600 * 8,

        timerInterval=1,

        showWorkTill=False,

        showDateTime=False,

        logPath="{0}/{1}".format(getSettingsFolder(_appName), "log.txt"),

        projectsDataPath="{0}/{1}".format(getSettingsFolder(_appName), "projects"),

        slackingDataPath="{0}/{1}".format(getSettingsFolder(_appName), "slacking"),

        logEditCommand="open -a TextEdit \"%s\"",

        projectSeparator="::",

        selectedProject="Default",

        startPlaceholder="__start__",

        showNotification=False,

        notificationTime=40,

        notificationRepeatTime=10,

        soundOnNotification=False,

        showHelpMessageOnStart=True,

        loggingLevel=logging.INFO,

        loggingFormat='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s'

    )

    _globalSettings = {}

    def __init__(self):
        self._settingsFile = "%s/%s" % (getSettingsFolder(self._appName), "settings")
        self._conn = Connection(FileStorage(self._settingsFile))
        self._globalSettings = self._conn.get_root()

    def __getattr__(self, key):
        return self.get(key)

    def get(self, key):
        """Return setting value by key"""
        return self._globalSettings.get(key, self._defaultSettings[key])

    def set(self, key, value):
        """Set setting value by key"""
        self._globalSettings[key] = value

    def sync(self):
        self._conn.commit()

    def __del__(self):
        self.sync()

Settings = _Settings()

