#
#  SlackingTasks.py
#  Class for storing slacking tasks
#
#  Copyright 2009 Artem Yunusov. All rights reserved.
#

from durus.file_storage import FileStorage
from durus.connection import Connection

from settings import SLACKING_DATA_PATH


class _SlackingAutocompletes(object):

    def __init__(self):
        self._conn = Connection(FileStorage(SLACKING_DATA_PATH))
        self._data = self._conn.get_root()

    def get(self):
        """Return slacking autocomplete list"""
        return self._data

    def add(self, name):
        """Add slacking autocomplete"""
        if name in self._data:
            self._data[name] += 1
        else:
            self._data[name] = 1
        self._conn.commit()

SlackingAutocompletes = _SlackingAutocompletes()
