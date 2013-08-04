#
#  log_util.py
#  Log initialization routines
#

import sys
import os
import logging
import traceback
from os.path import expanduser

from settings import Settings


def _excepthook(ex_cls, ex, tb):
    logger = logging.getLogger('mactimelog')

    logger.error('{0}: {1}\n{2}'.format(
            getattr(ex_cls, '__name__', ex_cls), ex,
            ''.join(traceback.format_tb(tb)).strip()))

    return sys.__excepthook__(ex_cls, ex, tb)


def init():

    sys.excepthook = _excepthook

    logger = logging.getLogger('mactimelog')

    logs_dir = '{0}/Library/Logs/MacTimeLog/'.format(expanduser('~'))

    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    handler = logging.FileHandler('{0}MacTimeLog.log'.format(logs_dir))

    formatter = logging.Formatter(Settings.loggingFormat)
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(Settings.loggingLevel)
