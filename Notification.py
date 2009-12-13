import os
import sys
from datetime import datetime
import objc
from Foundation import *
from AppKit import *
from Settings import Settings
from FormatterHelpers import secToMinutes

class GrowlWrapper(NSObject):
    
    def init(self, name):
        self = super(GrowlWrapper, self).init()
        self.name = name
        objc.loadBundle("GrowlApplicationBridge", globals(),
                         bundle_path=objc.pathForFramework(os.path.dirname(sys.argv[0]) + '/../Frameworks/Growl.framework'))

        self._growl = GrowlApplicationBridge
        self._growl.setGrowlDelegate_(self)
        self._callback = lambda context:None
        return self
        
    def growlNotificationWasClicked_(self, context):
        self._callback(context)
        
    def setCallback(self, callback):
        self._callback = callback
        
    def notify(self, title, description):
        self._growl.notifyWithTitle_description_notificationName_iconData_priority_isSticky_clickContext_(title, 
                                                                                                          description, self.name,None,
                                                                                                          0,False,NSDate.date())
                                                                                                          
class Notification(object):    
    
    def __init__(self, callback):
        self._notificator = GrowlWrapper.alloc().init("MacTimeLog")
        self._title = "MacTimeLog"
        self._last = datetime.now()
        self._notificator.setCallback(callback)
        
    def idleNotify(self, idleSeconds):
        if not Settings.get("showNotification"):
            self._last = datetime.now()
            
        elif secToMinutes(idleSeconds) >= Settings.get("notificationTime") \
        and secToMinutes((datetime.now() - self._last).seconds) >= Settings.get("notificationRepeatTime"):
            self._notificator.notify(self._title, "What are you workig on?")
            self._last = datetime.now()
        