# 
#  ReportsController.py
#  Report controller
#  
#  Copyright 2009 Artem Yunusov. All rights reserved.
# 
import datetime
import objc
from Foundation import *
from Settings import Settings
from Statistics import Statistics
from FormatterHelpers import secToTimeStr, nsDateToDatetime
from Timings import Timings

class ReportsController(NSWindowController):
    
    attributeBox = objc.IBOutlet("attributeBox")
    
    graphView = objc.IBOutlet("graphView")
    
    scrollView = objc.IBOutlet("scrollView")
    
    lblWorkTotal = objc.IBOutlet("lblWorkTotal")
    
    lblAvgWork = objc.IBOutlet("lblAvgWork")
    
    lblSlackTotal = objc.IBOutlet("lblSlackTotal")
    
    lblAvgSlack = objc.IBOutlet("lblAvgSlack")
    
    sgmControl = objc.IBOutlet("sgmControl")
    
    dpkrFrom = objc.IBOutlet("dpkrFrom")
    
    dpkrTo = objc.IBOutlet("dpkrTo")
    
    btnShow = objc.IBOutlet("btnShow")
    
    startDate = Timings.workStartDateTime() 
    
    endDate = Timings.workStartDateTime() + datetime.timedelta(days=1)
    
    reportType = "tasks"
    
    def init(self):
        return super(ReportsController, self).initWithWindowNibName_("Reports")
    
    def showWindow_(self, sender):
        self.window().makeKeyAndOrderFront_(sender)

    def awakeFromNib(self):
        self.window().setFrameAutosaveName_("reportsWindow")
        self.customControls = [self.btnShow, self.dpkrTo, self.dpkrFrom]
        self.dpkrTo.setDateValue_(NSDate.alloc().init())
        self.dpkrFrom.setDateValue_(NSDate.alloc().init())
        self.graphView.setConversionFunction(secToTimeStr)
        self.generateChart()
    
        
    def setDate(self, date):
        self.startDate = date
        self.endDate = Timings.workStartDateTime() + datetime.timedelta(days=1)
        
    def updateState(self):
        self.setCustomControlsEnabled(False)
        self.generateChart()
        
    def setCustomControlsEnabled(self, enabled):
        for control in self.customControls:
            control.setEnabled_(enabled)    
        
    def generateChart(self):
        self.graphView.setScrollView(self.scrollView)

        stat = Statistics(self.startDate, self.endDate)
        
        if self.reportType == "tasks":
            self.graphView.setData(stat.countTasks(), self.reportType) 
                
        elif self.reportType == "projects":
            self.graphView.setData(stat.countProjects(), self.reportType) 
                
        elif self.reportType == "slacking":
            self.graphView.setData(stat.countSlacking(), self.reportType) 
    
        self.graphView.setScale(stat.maxValue)
        self.lblWorkTotal.setStringValue_(secToTimeStr(stat.totalWork))
        self.lblAvgWork.setStringValue_(secToTimeStr(stat.avgWork))
        self.lblSlackTotal.setStringValue_(secToTimeStr(stat.totalSlacking))
        self.lblAvgSlack.setStringValue_(secToTimeStr(stat.avgSlacking))
        self.graphView.setNeedsDisplay_(True)

#    def windowDidBecomeMain_(self, sender):
#        self.generateChart()
        
    @objc.IBAction  
    def customMenu_(self, sender):
        self.setCustomControlsEnabled(True)
        
    @objc.IBAction  
    def todayMenu_(self, sender):
        self.setDate(Timings.workStartDateTime())
        self.updateState()
        
    @objc.IBAction  
    def yeaterdayMenu_(self, sender):
        self.startDate = Timings.workStartDateTime() - datetime.timedelta(days=1)
        self.endDate = Timings.workStartDateTime() 
        self.updateState()
    
    @objc.IBAction
    def currentMonthMenu_(self, sender):
        today = Timings.workStartDateTime()
        d = today - datetime.timedelta(days=int(today.strftime("%d")) - 1)
        self.setDate(d)
        self.updateState()

    @objc.IBAction
    def currentWeekMenu_(self, sender):
        today = Timings.workStartDateTime()
        weekNumber = int(today.strftime("%w"))
        if weekNumber == 0: 
            weekNumber = 7
        d = today - datetime.timedelta(days=weekNumber - 1)
        self.setDate(d)
        self.updateState()

    @objc.IBAction
    def days20Menu_(self, sender):
        self.setDate(Timings.workStartDateTime() - datetime.timedelta(days=20))
        self.updateState()

    @objc.IBAction
    def days30Menu_(self, sender):
        self.setDate(Timings.workStartDateTime() - datetime.timedelta(days=30))
        self.updateState()

    @objc.IBAction
    def days10_(self, sender):
        self.setDate(Timings.workStartDateTime() - datetime.timedelta(days=10))
        self.updateState()
        
    @objc.IBAction  
    def typeChanged_(self, sender):
        sel = self.sgmControl.selectedSegment()
        if sel == 0:
            self.reportType = "tasks"
        elif sel == 1:
            self.reportType = "projects"
        elif sel == 2:
            self.reportType = "slacking"
        self.generateChart()
        
    @objc.IBAction     
    def showCustom_(self, sender):
        self.startDate = Timings.combineDateWithTime(nsDateToDatetime(self.dpkrFrom.dateValue()))
                                  
        self.endDate = Timings.combineDateWithTime(nsDateToDatetime(self.dpkrTo.dateValue()) + 
                                                   datetime.timedelta(days=1))
        self.generateChart()
    