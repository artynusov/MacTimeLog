# 
#  Statistics.py
#  Statistic generator
#  
#  Copyright 2009 Artem Yunusov. All rights reserved.
# 
from DataManager import DataManager
from Timings import Timings
from Tasks import Tasks

class Statistics(object):
    
    _avgWork = 0
    _avgSlacking = 0
    _maxValue = 0
    
    def __init__(self, fromDate, toDate):
        self.timings = Timings()
        self._fromDate = fromDate
        self._toDate = toDate
        
    def _countAttrib(self, res):
        """Count basic attributes(average work, average slacking and maximum value)"""
        days = (self._toDate - self._fromDate).days
        self._avgWork = int(self.timings.spentSeconds / days)
        self._avgSlacking = int(self.timings.slackingSeconds / days)
        if res:
            self._maxValue = max(res)
        
    def _countObject(self, objType, targetAction):
        """Generic function for calculating projects data or slacking statistics"""
        self._data = DataManager.getByRange(self._fromDate, self._toDate)
        res = {}

        for date, task, projectName in self._data:
            if task == "__start__":
                self.timings.setPrevDate(None)
            objKey = projectName if objType == "project" else task
            
            spentSeconds = self.timings.count(date, Tasks.taskType(task))

            if Tasks.taskType(task) != targetAction:
                self.timings.setPrevDate(date)
                continue

            if spentSeconds:
                if objKey not in res:
                    res[objKey] = spentSeconds
                else:
                    res[objKey] += spentSeconds
                    
        self._countAttrib(res.values())
        if res:
            return sorted(res.iteritems(), key=lambda item:item[1], reverse=True)
        else:
            return []
        
    def countProjects(self):
        """Count project statistics"""
        return self._countObject("project", "work")
            
    def countSlacking(self):
        """Count slacking statistics"""
        return self._countObject("task", "slack")
            
    def countTasks(self):
        """Count tasks statistics divided by projects"""
        self._data = DataManager.getByRange(self._fromDate, self._toDate)
        res = {}
        for date, task, projectName in self._data:
            if task == "__start__":
                self.timings.setPrevDate(None)
            
            spentSeconds = self.timings.count(date, Tasks.taskType(task))
            
            if Tasks.taskType(task) != "work":
                continue
                
            if spentSeconds:
                if projectName not in res:
                    res[projectName] = {}
                    
                if task not in res[projectName]:
                    res[projectName][task] = spentSeconds
                else:
                    res[projectName][task] += spentSeconds
        self._countAttrib([v for k in res for v in res[k].values()])
        if res:
            ret = {}
            for k in res.keys():
                ret[k] = sorted(res[k].iteritems(), key=lambda item:item[1], reverse=True)
            return ret
        else:
            return {}
        
    @property
    def maxValue(self):
        """Maximum value of calculated object (project /task / slackings)"""
        return self._maxValue
    
    @property
    def totalWork(self):
        """Total work done"""
        return self.timings.spentSeconds
        
    @property
    def avgWork(self):
        """Average work per day"""
        return self._avgWork
    
    @property
    def totalSlacking(self):
        """Total slacking"""
        return self.timings.slackingSeconds
    
    @property
    def avgSlacking(self):
        """Average slacking per day"""
        return self._avgSlacking