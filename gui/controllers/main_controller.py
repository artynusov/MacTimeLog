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

import settings
from user_prefs import userPrefs

from tasks import Tasks
from tasks.projects import Projects
from tasks.slacking_autocompletes import SlackingAutocompletes
import common.formatter_helpers as fh

from common.notification import Notification
from common.decorators import memoize
from reports_controller import ReportsController
from preferences_controller import PreferencesController


class MainController(NSObject):

    outputArea = objc.IBOutlet("outputArea")

    lblTimeLeft = objc.IBOutlet("lblTimeLeft")

    lblTimeSpentCurr = objc.IBOutlet("lblTimeSpentCurr")

    cbxInput = objc.IBOutlet("cbxInput")

    lblSlackingTime = objc.IBOutlet("lblSlackingTime")

    lblTimeSpent = objc.IBOutlet("lblTimeSpent")

    lblWorkTill = objc.IBOutlet("lblWorkTill")

    pbtnProject = objc.IBOutlet("pbtnProject")

    workTillBox = objc.IBOutlet("workTillBox")

    mainWindow = objc.IBOutlet("mainWindow")

    applicationRef = objc.IBOutlet("applicationRef")

    btnDone = objc.IBOutlet("btnDone")

    reportWindow = None

    tasks = None

    @property
    @memoize
    def reportsController(self):
        controller = ReportsController.alloc().init()
        self.reportWindow = controller.window()
        return controller

    @property
    @memoize
    def preferencesController(self):
        return PreferencesController.alloc().initWithMainContorller(self)

    def awakeFromNib(self):
        def onGrowlClick():
            self.applicationRef.unhide()
            self.cbxInput.becomeFirstResponder()

        self.notification = Notification(onGrowlClick)
        self.initControls()
        self.initWindow()
        self.readCounters()
        self._timer = (NSTimer.
            scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
                userPrefs.timerInterval, self, self.timerFunction, None, True))

    def initControls(self):
        """Init basic controls"""
        self.outputArea.setString_("")

        self.tasks = Tasks()

        if userPrefs.showWorkTill:
            self.workTillBox.setHidden_(False)
        else:
            self.workTillBox.setHidden_(True)

        self.pbtnProject.removeAllItems()
        self.pbtnProject.addItemsWithTitles_(Projects.get())
        self.pbtnProject.selectItemWithTitle_(userPrefs.selectedProject)

        self.projectChange_(None)

        self.initDoneButton()

        self.fillTasks()
        self.scrollToEnd()

    def initDoneButton(self):
        if self.tasks.dayStarted():
            self.btnDone.setTitle_("Done")
        else:
            self.btnDone.setTitle_("Start")

    def initWindow(self):
        """Init window sizes and positions"""
        self.mainWindow.setFrameAutosaveName_("mainWindow")

    def timerFunction(self):
        """Timer callback function"""
        self.tasks.setCurrentTask(self.cbxInput.stringValue())
        self.readCounters()

        self.notification.idleNotify(self.tasks.timings.currentSeconds)

        if self.tasks.timings.isNextDay():
            self.initControls()

    def readCounters(self):
        """Read counters"""
        self.lblTimeSpent.setStringValue_(fh.secToTimeStr(
                self.tasks.timings.spentSeconds))
        self.lblSlackingTime.setStringValue_(fh.secToTimeStr(
                self.tasks.timings.slackingSeconds))
        self.lblTimeLeft.setStringValue_(fh.secToTimeStr(
                self.tasks.timings.leftSeconds))
        self.lblTimeSpentCurr.setStringValue_(fh.secToTimeStr(
                self.tasks.timings.currentSeconds))
        self.lblWorkTill.setStringValue_(fh.timeStructToTimeStr(
                self.tasks.timings.workTillTime))

    def appendTask(self, taskString, color):
        def appendText(text, color=None):
            """Append text to task text area"""
            endRange = NSRange()
            endRange.location = self.outputArea.textStorage().length()
            endRange.length = 0
            self.outputArea.replaceCharactersInRange_withString_(endRange, text)
            if color:
                colorRange = NSRange()
                colorRange.location = (
                        self.outputArea.textStorage().length() - len(text))
                colorRange.length = len(text)
                self.outputArea.setTextColor_range_(color, colorRange)
        appendText(taskString, color)

        if self.reportWindow and self.reportWindow.isVisible():
            self.reportsController.generateChart()

    def fillTasks(self):
        """Fill text area with tasks"""
        for task in self.tasks.taskList:
            self.appendTask(*fh.formatTaskString(*task))

    def scrollToEnd(self):
        """Scroll tasks textarea to the end"""
        self.outputArea.scrollRangeToVisible_(
                NSMakeRange(self.outputArea.string().length(), 0))

    def showStartHelpMessage(self):
        """Show alert with help message"""
        alert = NSAlert.alloc().init()
        alert.addButtonWithTitle_('OK')
        alert.setMessageText_("Congrats, you started your working day!")
        alert.setInformativeText_("Now start doing your working activity "
                "(e.g reading mail). When you finish with your activity "
                "go back to MacTimeLog and type it in. If your activity is "
                "slacking, use 2 asterisks (**) at the end of the activity's "
                "name.")
        alert.setShowsSuppressionButton_(True)
        alert.runModal()
        if alert.suppressionButton().state() == NSOnState:
            userPrefs.showHelpMessageOnStart = False
            userPrefs.save()

    @objc.IBAction
    def btnDonePress_(self, sender):
        """On done button press"""
        if self.tasks.dayStarted():
            if self.cbxInput.stringValue().strip():
                taskName = self.cbxInput.stringValue()
                self.appendTask(*fh.formatTaskString(
                        *self.tasks.add(taskName,
                            self.pbtnProject.titleOfSelectedItem())))
                self.readCounters()
                self.cbxInput.setStringValue_("")
                self.scrollToEnd()

                if Tasks.taskType(taskName) == "work":
                    Projects.addAutocomplete(
                            self.pbtnProject.titleOfSelectedItem(), taskName)
                else:
                    SlackingAutocompletes.add(taskName)
                self.cbxInput.addItemWithObjectValue_(taskName)
        else:
            if userPrefs.showHelpMessageOnStart:
                self.showStartHelpMessage()
            taskName = userPrefs.startPlaceholder
            self.appendTask(*fh.formatTaskString(*self.tasks.add(taskName)))
            self.initDoneButton()

    @objc.IBAction
    def projectChange_(self, sender):
        """Project changed event"""
        if self.pbtnProject.titleOfSelectedItem():
            self.cbxInput.removeAllItems()
            self.cbxInput.addItemsWithObjectValues_(Projects.getAutocomleteList(
                    self.pbtnProject.titleOfSelectedItem(),
                    SlackingAutocompletes.get()))

        if sender:
            userPrefs.selectedProject = unicode(
                    self.pbtnProject.titleOfSelectedItem())
            userPrefs.save()

    @objc.IBAction
    def openLog_(self, sender):
        """ Open log in text editor"""
        os.system(userPrefs.logEditCommand % settings.LOG_PATH)

    @objc.IBAction
    def openReports_(self, sender):
        """Open reports window"""
        self.reportsController.showWindow_(sender)

    @objc.IBAction
    def openPreferences_(self, sender):
        """Open preferences window"""
        self.preferencesController.showWindow_(sender)
