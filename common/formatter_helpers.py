#
#  FormatterHelper.py
#  Bscic conversion functions
#
#  Copyright 2009 Artem Yunusov. All rights reserved.
#

import time
from Foundation import *
from AppKit import *
from datetime import datetime

from user_prefs import userPrefs


def secToHrsMinsTuple(sec):
    """Convert seconds to hour/minutes tuple"""
    hours = int(sec) / 3600
    minutes = int(sec) % 3600 / 60
    return (hours, minutes)


def secToHours(sec):
    """Convert seconds to hours"""
    return int(sec) / 3600.


def secToMinutes(sec):
    """Convert seconds to mintes"""
    return int(sec) / 60.


def hoursToSeconds(hrs):
    """Convert seconds to hours"""
    return int(hrs) * 3600


def secToTimeStr(sec):
    """Convert seconds to time string"""
    return "%02d:%02d" % secToHrsMinsTuple(sec)


def timeStructToTimeStr(timeStruct):
    """Convert time_struct to time string"""
    return time.strftime(userPrefs.timeFormat, timeStruct)


def datetimeToNSDate(dt):
    """ Convert from datetime.datetime to NSDate """
    utime = time.mktime(dt.timetuple())
    return NSDate.dateWithTimeIntervalSince1970_(utime)


def nsDateToDatetime(nsdate):
    """Convert NSDate value to datetime"""
    return datetime.fromtimestamp(nsdate.timeIntervalSince1970())


def formatTaskString(date, task, projectName, spentSeconds, taskType):
    """Format task string"""
    if taskType == "work":
        color = NSColor.blackColor()
    elif taskType == "slack":
        color = NSColor.grayColor()
    else:
        color = NSColor.colorWithCalibratedRed_green_blue_alpha_(.72,.72,.72, 1)

    if spentSeconds is None: # Start of the day
        taskString = "Your working day started on %s \n" % date.strftime("%c")
        return taskString, color
    else:
        dtStr = ""
        if userPrefs.showDateTime:
            dtStr = " " + date.strftime(userPrefs.logDateTimeFormat)
        project = ""
        if projectName != "" and projectName != "Default" and taskType == "work":
            project = "%s %s " % (projectName, userPrefs.projectSeparator)
        return "%s%s  >>  %s%s \n" % (secToTimeStr(spentSeconds), dtStr, project, task), color
