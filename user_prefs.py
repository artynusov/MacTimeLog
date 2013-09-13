import logging
from ConfigParser import ConfigParser, NoOptionError, NoSectionError

import settings

from common.functional import LazyObject


logger = logging.getLogger('user_prefs')


class types(object):
    str = 'get'
    bool = 'getboolean'
    int = 'getint'
    float = 'getfloat'


class UserPrefs(object):

    defaults = dict(

        logDateTimeFormat = ("at %H:%M", types.str),

        showWorkTill = (True, types.bool),

        logEditCommand = ('open -a TextEdit "%s"', types.str),

        showHelpMessageOnStart = (True, types.bool),

        dateFormat = ('%m-%d-%Y %H:%M', types.str),

        projectSeparator = ('::', types.str),

        timeFormat = ('%H:%M', types.str),

        workEndTime = ('06:00', types.str),

        workDayLength = (3600 * 8, types.int),

        timerInterval = (1, types.int),

        showDateTime = (False, types.bool),

        selectedProject = ('Default', types.str),

        soundOnNotification = (False, types.bool),

        notificationRepeatTime = (10, types.int),

        notificationTime = (40, types.int),

        showNotification = (False, types.bool),

        startPlaceholder = ("__start__", types.str),

    )

    root_section = 'root'

    def __init__(self):
        self.config = ConfigParser()
        self.config.read(settings.USER_PREFS_PATH)
        if not self.config.has_section(self.root_section):
            self.config.add_section(self.root_section)

    def __getattr__(self, name):
        if name not in self.defaults:
            raise ValueError("No such prefernce '{0}'".format(name))

        default, type_name = self.defaults[name]

        try:
            try:
                value = getattr(self.config, type_name)(
                    self.root_section, name)
            except (TypeError, ValueError):
                logger.warn("Unable to cast type for '{0}', using default value".
                            format(name, value))
                value = default

        except NoOptionError:
            value = default

        return value

    def __setattr__(self, name, value):
        if name in self.defaults:
            self.config.set(self.root_section, name, unicode(value))
        else:
            super(UserPrefs, self).__setattr__(name, value)

    def save(self):
        with open(settings.USER_PREFS_PATH, 'wb') as configfile:
            self.config.write(configfile)


userPrefs = LazyObject(UserPrefs)