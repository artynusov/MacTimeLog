# 
#  MainController.py
#  Main application controller
#  
#  Copyright 2009 Artem Yunusov. All rights reserved.
# 
import os
import objc
from Foundation import *
from AppKit import *
from Tasks import Tasks
from Projects import Projects
from SlackingAutocompletes import SlackingAutocompletes
import FormatterHelpers as fh
from Settings import Settings


class MainController(NSObject):
    
    outputArea = objc.IBOutlet("outputArea")
    
    lblTimeLeft = objc.IBOutlet("lblTimeLeft")

    lblTimeSpentCurr = objc.IBOutlet("lblTimeSpentCurr")

    cbxInput = objc.IBOutlet("cbxInput")

    lblSlackingTime = objc.IBOutlet("lblSlackingTime")

    lblTimeSpent = objc.IBOutlet("lblTimeSpent")

    lblWorkTill = objc.IBOutlet("lblWorkTill")
    
    pbtnProject = objc.IBOutlet("pbtnProject")
    
    pbtnProject = objc.IBOutlet("pbtnProject")
    
    workTillBox = objc.IBOutlet("workTillBox")
    
    mainWindow = objc.IBOutlet("mainWindow")

    prefWindow = objc.IBOutlet("prefWindow")

    reportWindow = objc.IBOutlet("reportWindow")
    
    reportController = objc.IBOutlet("reportController")
    
    tasks = None
    
    def awakeFromNib(self):
        timeFormatter = fh.SecondsToTimeFormatter.alloc().init()
        timeStructFormatter = fh.TimeStructToTimeFormatter.alloc().init()
        
        self.lblTimeSpent.setFormatter_(timeFormatter)
        self.lblSlackingTime.setFormatter_(timeFormatter)
        self.lblTimeLeft.setFormatter_(timeFormatter)
        self.lblTimeSpentCurr.setFormatter_(timeFormatter)
        self.lblWorkTill.setFormatter_(timeStructFormatter)
        
        self.initControls()
        self.initWindowStates()
        self.readCounters()
        self._timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(Settings.get("timerInterval"), 
                      self, self.timerFunction, None, True)
                      
    def initControls(self):
        """Init basic controls"""
        self.outputArea.setString_("")
        
        self.tasks = Tasks()
        
        if Settings.get("showWorkTill"):
            self.workTillBox.setHidden_(False)
        else:
            self.workTillBox.setHidden_(True)
            
        self.pbtnProject.removeAllItems()
        self.pbtnProject.addItemsWithTitles_(Projects.get())
        self.pbtnProject.selectItemWithTitle_(Settings.get("selectedProject"))
        
        self.projectChange_(None)
        
        self.fillTasks()
        self.scrollToEnd()
        
    def initWindowStates(self):
        """Init windows sizes and positions"""
        self.prefWindow.setFrameAutosaveName_("prefWindow")
        self.mainWindow.setFrameAutosaveName_("mainWindow")
        self.reportWindow.setFrameAutosaveName_("reportWindow")
                  
    def timerFunction(self):
        """Timer callback function"""
        self.tasks.setCurrentTask(self.cbxInput.stringValue())
        self.readCounters()
        
    def readCounters(self):
        """Read counters"""
        self.lblTimeSpent.setStringValue_(self.tasks.timings.spentSeconds)
        self.lblSlackingTime.setStringValue_(self.tasks.timings.slackingSeconds)
        self.lblTimeLeft.setStringValue_(self.tasks.timings.leftSeconds)
        self.lblTimeSpentCurr.setStringValue_(self.tasks.timings.currentSeconds)
        
        self.lblWorkTill.setStringValue_(self.tasks.timings.workTillTime)

    def appendTask(self, taskString, color):
        def appendText(text, color=None):
            """Append text to task text area"""
            endRange = NSRange()
            endRange.location = self.outputArea.textStorage().length()
            endRange.length = 0
            self.outputArea.replaceCharactersInRange_withString_(endRange, text)
            if color:
                colorRange = NSRange()
                colorRange.location = self.outputArea.textStorage().length() - len(text) 
                colorRange.length = len(text)
                self.outputArea.setTextColor_range_(color, colorRange)
        appendText(taskString, color)
        
        if self.reportWindow.isVisible():
            self.reportController.generateChart()
            
    def fillTasks(self):
        """Fill text area with tasks"""
        for task in self.tasks.taskList:
            self.appendTask(*fh.formatTaskString(*task))
            
    def scrollToEnd(self):
        """Scroll tasks textarea to the end"""
        self.outputArea.scrollRangeToVisible_(NSMakeRange(self.outputArea.string().length(), 0))

    @objc.IBAction
    def btnDonePress_(self, sender):
        """On done button press"""
        if self.cbxInput.stringValue().strip():
            taskName = self.cbxInput.stringValue()
            self.appendTask(*fh.formatTaskString(*self.tasks.add(taskName, self.pbtnProject.titleOfSelectedItem())))
            self.readCounters()
            self.cbxInput.setStringValue_("")
            self.scrollToEnd()
            
            if  Tasks.taskType(taskName) == "work":
                Projects.addAutocomplete(self.pbtnProject.titleOfSelectedItem(), taskName)
            else:
                SlackingAutocompletes.add(taskName)
            self.cbxInput.addItemWithObjectValue_(taskName)

    @objc.IBAction
    def projectChange_(self, sender):
        """Project changed event"""
        if self.pbtnProject.titleOfSelectedItem():
            self.cbxInput.removeAllItems()
            self.cbxInput.addItemsWithObjectValues_(Projects.getAutocomleteList(
                                    self.pbtnProject.titleOfSelectedItem(), SlackingAutocompletes.get()))

        if sender:
            Settings.set("selectedProject", unicode(self.pbtnProject.titleOfSelectedItem()))
        Settings.sync()
        
    @objc.IBAction
    def openLog_(self, sender):
        """ Open log in text editor"""
        os.system(Settings.get("logEditCommand") % Settings.get("logPath"))
        