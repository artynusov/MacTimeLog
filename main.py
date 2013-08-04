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

from PyObjCTools import AppHelper

from common import log_util
log_util.init()

# import modules containing classes required to start application and load MainMenu.nib

from gui import application
from gui.delegates import app_delegate, main_window_delegate
from gui.controllers import main_controller, reports_controller, preferences_controller
from gui.views import graph_view

# pass control to AppKit
AppHelper.runEventLoop()