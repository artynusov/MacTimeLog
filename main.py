#
#  main.py
#  Main file
#
#  Copyright 2009 Artem Yunusov. All rights reserved.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

#import modules required by application
import objc
import Foundation
import AppKit

from PyObjCTools import AppHelper

# import modules containing classes required to start application and load MainMenu.nib

import MacTimeLogAppDelegate
import MacTimeLogApplication
import MainController
import GraphView
import ReportsController
import PreferencesController
import MainWindowDelegate

# pass control to AppKit
AppHelper.runEventLoop()
