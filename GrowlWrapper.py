import os
import sys
import objc
from Foundation import *
from AppKit import *


class GrowlWrapper(NSObject):
    
    def init(self, name="MacTimeLog"):
        self = super(GrowlWrapper, self).init()
        self.name = name
        objc.loadBundle("GrowlApplicationBridge", globals(),
                         bundle_path=objc.pathForFramework(os.path.dirname(sys.argv[0]) + '/../Frameworks/Growl.framework'))

        self._growl = GrowlApplicationBridge
        self._growl.setGrowlDelegate_(self)
        return self
        
    def growlNotificationWasClicked_(self, context):
        print context
        
    def notify(self, title, description):
        self._growl.notifyWithTitle_description_notificationName_iconData_priority_isSticky_clickContext_(title, 
                                                                                                          description, self.name,None,
                                                                                                          0,False,NSDate.date())
        