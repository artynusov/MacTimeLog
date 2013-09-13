from os.path import expanduser
import logging

from common.utils import getApplicationDirectory


APP_NAME = 'MacTimeLog'
APP_DIR = getApplicationDirectory(APP_NAME)

LOG_PATH = '{0}/{1}'.format(APP_DIR, 'log.txt')

USER_PREFS_PATH = '{0}/{1}'.format(APP_DIR, 'user_prefs.ini')
PROJECTS_DATA_PATH = '{0}/{1}'.format(APP_DIR, 'projects')
SLACKING_DATA_PATH = '{0}/{1}'.format(APP_DIR, 'slacking')

LOGGING_LEVEL = logging.INFO
LOGGING_FORMAT = '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s'
LOGGING_DIR = '{0}/Library/Logs/MacTimeLog/'.format(expanduser('~'))

try:
    from local_setings import *
except ImportError:
    pass
