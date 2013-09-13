#
#  projects.py
#  Class for working with projects
#
#  Copyright 2009 Artem Yunusov. All rights reserved.
#

from durus.file_storage import FileStorage
from durus.connection import Connection
from durus.persistent_dict import PersistentDict

from settings import PROJECTS_DATA_PATH


class _Projects(object):
    """
    Class for managing project and autocompletes
    for each project
    """

    def __init__(self):
        self._conn = Connection(FileStorage(PROJECTS_DATA_PATH))
        self._data = self._conn.get_root()

        if not len(self._data.keys()):
            self._data["Default"] = PersistentDict(autocomplete=PersistentDict())
            self.sync()

    def get(self):
        """Return projects list"""
        return self._data.keys()

    def add(self, name):
        """Add new project"""
        self._data[unicode(name)] = PersistentDict(autocomplete=PersistentDict())
        self.sync()

    def remove(self, name):
        """Remove project"""
        del self._data[unicode(name)]

    def getAutocomleteList(self, name, appendix={}):
        """
        Return autocomplete list for project, if appendix
        autocompletes was specified merge it with project autocompletes.
        """
        autocompDict = self._data[unicode(name)]["autocomplete"]
        autocompDict.update(appendix)
        sortedDict = sorted(autocompDict.items(), key=lambda (k, v):(v, k), reverse=True)
        return [a[0] for a in sortedDict]

    def addAutocomplete(self, projectName, taskName):
        """Add autocompleted task for peoject"""
        prj = self._data[projectName]
        if taskName not in prj["autocomplete"]:
            prj["autocomplete"][taskName] = 1
        else:
            prj["autocomplete"][taskName] += 1
        self.sync()

    def sync(self):
        self._conn.commit()

    def __del__(self):
        self.sync()

Projects = _Projects()


