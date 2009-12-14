from AppKit import *
from Carbon.CarbonEvt import RegisterEventHotKey, GetApplicationEventTarget
from Carbon.Events import cmdKey, controlKey

kEventHotKeyPressedSubtype = 6


class MacTimeLogApplication(NSApplication):

    def finishLaunching(self):
        super(MacTimeLogApplication, self).finishLaunching()        
        self.hotKeyRef = RegisterEventHotKey(46, cmdKey+controlKey , (0, 0),
                                             GetApplicationEventTarget(), 0)
    
    def sendEvent_(self, theEvent):
        if theEvent:
            if theEvent.type() == NSSystemDefined and \
                   theEvent.subtype() == kEventHotKeyPressedSubtype:
               
                self.activateIgnoringOtherApps_(True)

                if self.isHidden():
                    self.unhide()
                else:
                    if self.isActive():
                        self.hide_(self)
                    else:
                        self.unhide()
        super(MacTimeLogApplication, self).sendEvent_(theEvent)
