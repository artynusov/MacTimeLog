#
#  preferences_controller.py
#  Preferences controller
#
#  Copyright 2009 Artem Yunusov. All rights reserved.
#

import datetime
import re
import objc
from Foundation import *
from AppKit import *

import settings
from user_prefs import userPrefs

from tasks.projects import Projects
import common.formatter_helpers as fh


class PreferencesController(NSWindowController):

    stprWorkHours = objc.IBOutlet("stprWorkHours")

    edtWorkHours = objc.IBOutlet("edtWorkHours")

    stprNotificationTime = objc.IBOutlet("stprNotificationTime")

    edtNotificationTime = objc.IBOutlet("edtNotificationTime")

    stprNotificationRepeatTime = objc.IBOutlet("stprNotificationRepeatTime")

    edtNotificationRepeatTime = objc.IBOutlet("edtNotificationRepeatTime")

    dpkrWorkStarts = objc.IBOutlet("dpkrWorkStarts")

    edtLogEditCommand = objc.IBOutlet("edtLogEditCommand")

    pbtnRemoveProject = objc.IBOutlet("pbtnRemoveProject")

    edtAddProject = objc.IBOutlet("edtAddProject")

    stprWorkHours = objc.IBOutlet("stprWorkHours")

    edtDateTimeFormat = objc.IBOutlet("edtDateTimeFormat")

    chbShowWorkTill = objc.IBOutlet("chbShowWorkTill")

    chbShowNotification = objc.IBOutlet("chbShowNotification")

    chbShowDateTime = objc.IBOutlet("chbShowDateTime")

    chbSoundOnNotification = objc.IBOutlet("chbSoundOnNotification")

    btnPreviewPopup = objc.IBOutlet("btnPreviewPopup")

    def initWithMainContorller(self, mainController):
        self.mainController = mainController
        return super(PreferencesController, self).initWithWindowNibName_("Preferences")

    def showWindow_(self, sender):
        self.window().makeKeyAndOrderFront_(sender)

    def awakeFromNib(self):
        self.window().setFrameAutosaveName_("prefWindow")
        self.initVlaues()
        self.loadProjectsLists()

    def initVlaues(self):
        self.stprWorkHours.setIntValue_(fh.secToHours(userPrefs.workDayLength))
        self.edtWorkHours.setIntValue_(self.stprWorkHours.intValue())

        self.stprNotificationTime.setIntValue_(userPrefs.notificationTime)
        self.edtNotificationTime.setIntValue_(self.stprNotificationTime.intValue())

        self.stprNotificationRepeatTime.setIntValue_(userPrefs.notificationRepeatTime)
        self.edtNotificationRepeatTime.setIntValue_(self.stprNotificationRepeatTime.intValue())

        workEndTime = datetime.datetime.strptime(userPrefs.workEndTime, "%H:%M").time()
        someDate = datetime.datetime.combine(datetime.datetime.now(), workEndTime)

        self.dpkrWorkStarts.setDateValue_(fh.datetimeToNSDate(someDate))

        self.edtLogEditCommand.setStringValue_(userPrefs.logEditCommand)

        self.chbShowWorkTill.setState_(1 if userPrefs.showWorkTill else 0)
        self.chbShowDateTime.setState_(1 if userPrefs.showDateTime else 0)
        self.chbShowNotification.setState_(1 if userPrefs.showNotification else 0)
        self.chbSoundOnNotification.setState_(1 if userPrefs.soundOnNotification else 0)

        self.edtDateTimeFormat.setStringValue_(userPrefs.logDateTimeFormat)
        self.edtDateTimeFormat.setEnabled_(self.chbShowDateTime.state())
        self.showNotification_(self)

    def saveSettings(self):
        userPrefs.workDayLength = fh.hoursToSeconds(
                self.stprWorkHours.intValue())

        userPrefs.workEndTime = fh.nsDateToDatetime(
                self.dpkrWorkStarts.dateValue()).strftime("%H:%M")

        userPrefs.logEditComman = self.edtLogEditCommand.stringValue()

        userPrefs.logDateTimeFormat = self.edtDateTimeFormat.stringValue()

        userPrefs.notificationTime = self.stprNotificationTime.intValue()

        userPrefs.notificationRepeatTime = (self.
                stprNotificationRepeatTime.intValue())

        userPrefs.save()

    def windowShouldClose_(self, sender):
        self.saveSettings()
        self.mainController.initControls()
        sender.orderOut_(sender)
        return False

    def loadProjectsLists(self):
        self.pbtnRemoveProject.removeAllItems()
        self.pbtnRemoveProject.addItemsWithTitles_(Projects.get())

    @objc.IBAction
    def addProject_(self, sender):
        projectName = self.edtAddProject.stringValue()
        if projectName not in Projects.get() and not re.match("^\s*$", projectName):
                Projects.add(self.edtAddProject.stringValue())
        else:
            # show alert with reason for failure
            alert = NSAlert.alloc().init()
            alert.addButtonWithTitle_('OK')
            alert.setMessageText_('Failed to add new project')
            alert.setInformativeText_('Please ensure the project does not '
                    'already exist and that it contains characters.')
            alert.runModal()

        self.loadProjectsLists()
        self.edtAddProject.setStringValue_('')

    @objc.IBAction
    def removeProject_(self, sender):
        Projects.remove(self.pbtnRemoveProject.titleOfSelectedItem())
        self.loadProjectsLists()

    @objc.IBAction
    def showDateTime_(self, sender):
        self.edtDateTimeFormat.setEnabled_(self.chbShowDateTime.state())
        userPrefs.showDateTime = bool(self.chbShowDateTime.state())

    @objc.IBAction
    def showWorkTill_(self, sender):
        userPrefs.showWorkTill = bool(self.chbShowWorkTill.state())

    @objc.IBAction
    def soundOnNotificaiton_(self, sender):
        userPrefs.soundOnNotification = bool(self.chbSoundOnNotification.state())

    @objc.IBAction
    def showNotification_(self, sender):
        result = bool(self.chbShowNotification.state())
        userPrefs.showNotification = result
        self.stprNotificationTime.setEnabled_(result)
        self.edtNotificationTime.setEnabled_(result)
        self.stprNotificationRepeatTime.setEnabled_(result)
        self.edtNotificationRepeatTime.setEnabled_(result)
        self.chbSoundOnNotification.setEnabled_(result)
        self.btnPreviewPopup.setEnabled_(result)

    @objc.IBAction
    def previewPopup_(self, sender):
        self.mainController.notification.notify("Test notification")
