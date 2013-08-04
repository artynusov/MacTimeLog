#
#  main_window_delegate.py
#  Window delegate, preventing close
#
#  Copyright 2009 Artem Yunusov. All rights reserved.
#

from AppKit import *
from Foundation import *

class MainWindowDelegate(NSWindow):

    def windowShouldClose_(self, sender):
        return False