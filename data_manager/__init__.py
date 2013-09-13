#
#  DataManager.py
#  Data manager
#
#  Copyright 2009 Artem Yunusov. All rights reserved.
#
from datetime import datetime

import settings
from user_prefs import userPrefs

from plain_text_driver import PlainTextDriver


class _DataManager(object):
    _driver = PlainTextDriver(settings.LOG_PATH,
            userPrefs.dateFormat, 16, userPrefs.projectSeparator)

    def writeTask(self, data, task, projectName, firstToday=False):
        if firstToday:
            task = userPrefs.startPlaceholder
            projectName = None
        self._driver.writeTask(data, task, projectName)

    def getAfterDate(self, date1):
        return self._driver.getByRange(date1, datetime.now())

    def getByRange(self, *args):
        return self._driver.getByRange(*args)

DataManager = _DataManager()
