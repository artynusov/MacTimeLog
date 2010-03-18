# 
#  Tasks.py
#  Class for working with tasks
#  
#  Copyright 2009 Artem Yunusov. All rights reserved.
# 

from Timings import Timings
from DataManager import DataManager

TASK_TYPE = ("work", "slack", None)

class Tasks(object):
    
    def __init__(self):
        self.timings = Timings()
        self.tasks = []
        for date, task, projectName in DataManager.getAfterDate(Timings.workStartDateTime()):
            self.processTask(date, task, projectName)
        
    def processTask(self, date, task, projectName):
        spentSeconds = self.timings.count(date, self.taskType(task))
        attributes = (date, task, projectName, spentSeconds, self.taskType(task))
        self.tasks.append(attributes)
        return attributes
        
    def dayStarted(self):
        """Return True if working day started else False"""
        return bool(len(self.tasks))
    
    def add(self, task, projectName=None):
        date = Timings.now()
        
        if self.taskType(task) != "work":
            projectName = None
            
        attributes = self.processTask(date, task, projectName)
        DataManager.writeTask(date, task, projectName, firstToday=len(self.tasks) == 1)
        return attributes
        
    def setCurrentTask(self, task):
        self.timings.setCurrentTaskType(self.taskType(task))
        
    @property
    def taskList(self):
        return self.tasks
    
    @staticmethod        
    def taskType(taskString):
        return None if taskString.strip() == "" or taskString.find("***") != -1 \
                    else "work" if taskString.find("**") == -1 else "slack"

if __name__ == '__main__':
   pass
    
    
