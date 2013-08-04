# 
#  PlainTextDriver.py
#  Class for reading MacTimeLog log
#  
#  Copyright 2009 Artem Yunusov. All rights reserved.
# 

from __future__ import with_statement
import os
import datetime

class PlainTextDriver(object):
    
    def __init__(self, logPath, dateFormat, dateLength, projectSeparator):
        self._dateFormat = str(dateFormat)
        self._dateLength = dateLength
        self._projectSeparator = projectSeparator
        self._logPath = logPath
        if not os.path.exists(logPath):
            with open(logPath, "w") as log:
                pass
        self._log = ""
        
    def _readLog(self):
        with open(self._logPath) as log:
            self._log = log.read().decode("utf8")
            
    def writeTask(self, date, task, projectName):
        """Write task"""
        if projectName:
            data =  "%s   %s %s %s" % (date.strftime(self._dateFormat), projectName, self._projectSeparator, task)
        else:
            data =  "%s   %s" % (date.strftime(self._dateFormat), task)
            
        with open(self._logPath, "a") as log: 
            log.write(data.encode( "utf-8" ) + "\n")
    
    def getByRange(self, startDate, endDate):
        """Return day log"""
        self._readLog()
        lines = self._log.strip().split("\n")              
        buff = []
        for line in lines[::-1]:
            if line.strip().startswith("#"):
                continue
            if line.strip() and len(line) >= self._dateLength:
                date = datetime.datetime.strptime(line.strip()[0:self._dateLength], self._dateFormat)
                
                if date >= startDate and date <= endDate:
                    date = line[0:self._dateLength]
                    right = line[self._dateLength + 1:].strip()
                    prjIndex = right.find(self._projectSeparator)
                    if prjIndex == -1:
                        projectName = ""
                        taskName = right.strip()
                    else:
                        projectName = right[:prjIndex].strip()
                        taskName = right[prjIndex + len(self._projectSeparator):].strip()

                    buff.append((datetime.datetime.strptime(date, self._dateFormat), taskName, projectName))

        buff.reverse()
        return buff
        