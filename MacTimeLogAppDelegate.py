from Foundation import *
from AppKit import *
from Projects import Projects

class MacTimeLogAppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, sender):
        NSLog("Application did finish launching.")
        
    def applicationShouldTerminate_(self, sender):
        Projects.sync()
        return True