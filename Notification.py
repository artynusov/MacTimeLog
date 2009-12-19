import os
import sys
from datetime import datetime
from subprocess import Popen
import objc
from Foundation import *
from AppKit import *
from Settings import Settings
from FormatterHelpers import secToMinutes
from utils import run_in_thread


class GrowlWrapper(object):
    
    def __init__(self, appName):
        self.appName = appName
        self.growl_binary = os.path.dirname(sys.argv[0]) + '/../Resources/bin/growlnotify'
    
    @run_in_thread
    def notify(self, title, message):
        pool = NSAutoreleasePool.new()
        p1 = Popen(self.growl_binary + " --click -a '%s' -t '%s' -m '%s'" % (self.appName, title, message), shell=True)
        return_code = p1.wait()
        if return_code == 100:
            self.clickCallback()
        
    def setClickCallback(self, callback):
        self.clickCallback = callback

                                                                                                          
class Notification(object):    
    
    def __init__(self, callback):
        self._notificator = GrowlWrapper("MacTimeLog")
        self._title = "MacTimeLog"
        self._last = datetime.now()
        self._notificator.setClickCallback(callback)
        
    def playSound(self):
        try:
            systemSound = NSSound.soundNamed_("Hero")
            systemSound.play()
        except:
            pass
            
    def notify(self, text):
        self._notificator.notify(self._title, text)
        if Settings.get("soundOnNotification"):
            self.playSound()
        
    def idleNotify(self, idleSeconds):
        if not Settings.get("showNotification"):
            self._last = datetime.now()
            
        elif secToMinutes(idleSeconds) >= Settings.get("notificationTime") \
        and secToMinutes((datetime.now() - self._last).seconds) >= Settings.get("notificationRepeatTime"):
            self.notify("What are you working on?")
            self._last = datetime.now()
            