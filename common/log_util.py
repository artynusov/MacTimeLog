#
#  log_util.py
#  Log initialization routines
#

import sys
import os
import logging
import traceback

from settings import LOGGING_LEVEL, LOGGING_FORMAT, LOGGING_DIR


def _excepthook(ex_cls, ex, tb):
    logger = logging.getLogger('mactimelog')

    logger.error('{0}: {1}\n{2}'.format(
            getattr(ex_cls, '__name__', ex_cls), ex,
            ''.join(traceback.format_tb(tb)).strip()))

    return sys.__excepthook__(ex_cls, ex, tb)


def init():
    sys.excepthook = _excepthook

    logger = logging.getLogger('mactimelog')

    if not os.path.exists(LOGGING_DIR):
        os.makedirs(LOGGING_DIR)

    handler = logging.FileHandler('{0}MacTimeLog.log'.format(LOGGING_DIR))

    formatter = logging.Formatter(LOGGING_FORMAT)
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(LOGGING_LEVEL)
