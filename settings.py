import sys

from os.path import expanduser
import logging

from common.settings_utils import initAppDirs


# initAppDirs sets following settings:
#
# APP_NAME
# APP_DIR
# LOG_PATH
# USER_PREFS_PATH
# PROJECTS_DATA_PATH
# SLACKING_DATA_PATH
initAppDirs(sys.modules[__name__], 'MacTimeLog')

LOGGING_LEVEL = logging.INFO
LOGGING_FORMAT = '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s'
LOGGING_DIR = '{0}/Library/Logs/MacTimeLog/'.format(expanduser('~'))

try:
    from local_settings import *
except ImportError:
    pass
