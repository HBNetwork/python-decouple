# coding: utf-8
from ConfigParser import SafeConfigParser


class Config(object):
    """
    Wrapper around SafeConfigParser to deal with Django environment settings.
    """
    SECTION = 'settings'

    def __init__(self, config_file):
        self.load(config_file)

    def load(self, config_file):
        """
        Load config data from a file.
        """
        self.config_file = config_file
        self.parser = SafeConfigParser()
        self.parser.readfp(open(config_file))

    def get(self, option, default=u'', cast=unicode):
        """
        Return the value for option or default option is not defined.
        """
        if not self.parser.has_option(self.SECTION, option):
            return cast(default)

        getter = {
            bool: self.parser.getboolean,
            float: self.parser.getfloat,
            int: self.parser.getint,
        }.get(cast, self.parser.get)

        return cast(getter(self.SECTION, option))

    def __call__(self, *args, **kwargs):
        """
        Convenient shortcut to get.
        """
        return self.get(*args, **kwargs)

    def set(self, option, value):
        """
        Add a config value to configuration instance.
        """
        if not self.parser.has_section(self.SECTION):
            self.parser.add_section(self.SECTION)

        self.parser.set(self.SECTION, option, unicode(value))

    def remove(self, option):
        """
        Remove an option from the config instance.
        """
        return self.parser.remove_option(self.SECTION, option)

    def list(self):
        """
        Return a list of all (option, value) pairs.
        """
        return self.parser.items(self.SECTION)

    def save(self):
        """
        Persist current configuration instance to the original config file.
        """
        with open(self.config_file, 'wb') as f:
            self.parser.write(f)
