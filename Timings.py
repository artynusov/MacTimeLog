# 
#  Timings.py
#  Class for working with task timings
#  
#  Copyright 2009 Artem Yunusov. All rights reserved.
# 

import datetime
import time
from Settings import Settings

class Timings(object):
    
    _spent = 0
    _slacking = 0
    _prevDate = None
    _taskType = None
    
    def __init__(self):
        self._startDateTime = self.workStartDateTime()
    
    @property
    def spentSeconds(self):
        """Return time, spent on work"""
        possible = 0
        if self._taskType:
            possible = 0 if self._taskType == "slack" else self.currentSeconds
        return self._spent + possible
    
    @property
    def slackingSeconds(self):
        """Retrun slacking time"""
        possible = 0
        if self._taskType:
            possible = 0 if self._taskType == "work" else self.currentSeconds
        return self._slacking + possible
        
    @property
    def leftSeconds(self):
        """Return time left to work"""
        res = Settings.get("workDayLength") - self.spentSeconds
        if res < 0:
            return 0
        else:
            return res
            
    @property
    def currentSeconds(self):
        """Retrun curent task time"""
        if self._prevDate:
            return (Timings.now() - self._prevDate).seconds
        else:
            return 0
            
    @property    
    def workTillTime(self):
        """Return work till estimate"""
        currenttime = time.time()
        return time.localtime(currenttime + self.leftSeconds)

    @staticmethod
    def now():
        """Returren current datetime"""
        return datetime.datetime.now()
    
    @staticmethod  
    def workEndTime():
        return datetime.datetime.strptime(Settings.get("workEndTime"), "%H:%M").time()
            
    @staticmethod  
    def workStartDateTime():
        """ Return datetime object that represents start of the working day """
        workEndTime = Timings.workEndTime()
        cd = datetime.datetime.combine(Timings.now().date(), 
                                       workEndTime)
        if Timings.now().time() < workEndTime:
            cd -= datetime.timedelta(days=1)
        return cd
        
    @staticmethod
    def combineDateWithTime(date):
        """Combine date with work end/start time"""
        return datetime.datetime.combine(date, Timings.workEndTime())
        
    def setPrevDate(self, prevDate):
        """Set datetime of previous task"""
        self._prevDate = prevDate
    
    def setCurrentTaskType(self, taskType):
        """Set current task type"""
        self._taskType = taskType
    
    def count(self, date, taskType):
        """
        Increment counters
        Return seconds spent on task
        """
        if self._prevDate is None:
            self._prevDate = date
            return None
        else:
            currSpentSeconds = (date - self._prevDate).seconds
            if taskType == "slack":
                self._slacking += currSpentSeconds
            elif taskType == "work":
                self._spent += currSpentSeconds
            self._prevDate = date
            return currSpentSeconds
    
    def isNextDay(self):
        """Return true if program next working day started"""
        if self._startDateTime + datetime.timedelta(days=1) < self.now():
            return True
        else:
            return False
        
if __name__ == '__main__':
    t = Timings()

    
