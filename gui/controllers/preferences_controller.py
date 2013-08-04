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

from settings import Settings
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
        self.stprWorkHours.setIntValue_(fh.secToHours(Settings.get("workDayLength")))
        self.edtWorkHours.setIntValue_(self.stprWorkHours.intValue())

        self.stprNotificationTime.setIntValue_(Settings.get("notificationTime"))
        self.edtNotificationTime.setIntValue_(self.stprNotificationTime.intValue())

        self.stprNotificationRepeatTime.setIntValue_(Settings.get("notificationRepeatTime"))
        self.edtNotificationRepeatTime.setIntValue_(self.stprNotificationRepeatTime.intValue())

        workEndTime = datetime.datetime.strptime(Settings.get("workEndTime"), "%H:%M").time()
        someDate = datetime.datetime.combine(datetime.datetime.now(), workEndTime)
        self.dpkrWorkStarts.setDateValue_(fh.datetimeToNSDate(someDate))

        self.edtLogEditCommand.setStringValue_(Settings.get("logEditCommand"))

        self.chbShowWorkTill.setState_(1 if Settings.get("showWorkTill") else 0)
        self.chbShowDateTime.setState_(1 if Settings.get("showDateTime") else 0)
        self.chbShowNotification.setState_(1 if Settings.get("showNotification") else 0)
        self.chbSoundOnNotification.setState_(1 if Settings.get("soundOnNotification") else 0)

        self.edtDateTimeFormat.setStringValue_(Settings.get("logDateTimeFormat"))
        self.edtDateTimeFormat.setEnabled_(self.chbShowDateTime.state())
        self.showNotification_(self)

    def saveSettings(self):
        Settings.set("workDayLength", fh.hoursToSeconds(self.stprWorkHours.intValue()))
        dateStr = str(self.dpkrWorkStarts.dateValue())
        Settings.set("workEndTime", dateStr[11:16])
        Settings.set("logEditCommand", self.edtLogEditCommand.stringValue())
        Settings.set("logDateTimeFormat", self.edtDateTimeFormat.stringValue())
        Settings.set("notificationTime", self.stprNotificationTime.intValue())
        Settings.set("notificationRepeatTime", self.stprNotificationRepeatTime.intValue())
        Settings.sync()

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
            """Show alert with reason for failure"""
            alert = NSAlert.alloc().init()
            alert.addButtonWithTitle_('OK')
            alert.setMessageText_("Failed to add new project")
            alert.setInformativeText_("Please ensure the project does not already exist and that it contains characters.")
            alert.runModal()

        self.loadProjectsLists()
        self.edtAddProject.setStringValue_("")

    @objc.IBAction
    def removeProject_(self, sender):
        Projects.remove(self.pbtnRemoveProject.titleOfSelectedItem())
        self.loadProjectsLists()

    @objc.IBAction
    def showDateTime_(self, sender):
        self.edtDateTimeFormat.setEnabled_(self.chbShowDateTime.state())
        Settings.set("showDateTime", bool(self.chbShowDateTime.state()))

    @objc.IBAction
    def showWorkTill_(self, sender):
        Settings.set("showWorkTill", bool(self.chbShowWorkTill.state()))

    @objc.IBAction
    def soundOnNotificaiton_(self, sender):
        Settings.set("soundOnNotification", bool(self.chbSoundOnNotification.state()))

    @objc.IBAction
    def showNotification_(self, sender):
        result = bool(self.chbShowNotification.state())
        Settings.set("showNotification", result)
        self.stprNotificationTime.setEnabled_(result)
        self.edtNotificationTime.setEnabled_(result)
        self.stprNotificationRepeatTime.setEnabled_(result)
        self.edtNotificationRepeatTime.setEnabled_(result)
        self.chbSoundOnNotification.setEnabled_(result)
        self.btnPreviewPopup.setEnabled_(result)

    @objc.IBAction
    def previewPopup_(self, sender):
        self.mainController.notification.notify("Test notification")
