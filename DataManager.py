# 
#  DataManager.py
#  Data manager
#  
#  Copyright 2009 Artem Yunusov. All rights reserved.
# 
from datetime import datetime
from PlainTextDriver import PlainTextDriver
from Settings import Settings

class _DataManager(object):
    _driver = PlainTextDriver(Settings.get("logPath"), Settings.get("dateFormat"), 16, Settings.get("projectSeparator"))
    
    def writeTask(self, data, task, projectName, firstToday=False):
        if firstToday:
            task = Settings.get("startPlaceholder")
            projectName = None
        self._driver.writeTask(data, task, projectName)
        
    def getAfterDate(self, date1):
        return self._driver.getByRange(date1, datetime.now())
        
    def getByRange(self, *args):
        return self._driver.getByRange(*args)

DataManager = _DataManager()