import os
import threading

from Foundation import *


def run_in_thread(fn):
    def run(*k, **kw):
        t = threading.Thread(target=fn, args=k, kwargs=kw)
        t.start()
    return run


def getApplicationDirectory(appName):
    """Return appliction directory path"""
    paths = NSSearchPathForDirectoriesInDomains(NSApplicationSupportDirectory,
            NSUserDomainMask, True)
    basePath = (len(paths) > 0 and paths[0]) or NSTemporaryDirectory()
    fullPath = basePath.stringByAppendingPathComponent_(appName)

    if not os.path.exists(fullPath):
        os.makedirs(fullPath)
    return fullPath