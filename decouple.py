# coding: utf-8
import os
import sys
from ConfigParser import SafeConfigParser


class ConfigBase(object):
    """
    Base class to make the API explicit.
    """
    def __init__(self, config_file):
        raise NotImplemented

    def get(self, option, default=u'', cast=unicode):
        """
        Return the value for option or default option is not defined.
        """
        raise NotImplemented

    def __call__(self, *args, **kwargs):
        """
        Convenient shortcut to get.
        """
        return self.get(*args, **kwargs)


class ConfigIni(ConfigBase):
    """
    Wrapper around SafeConfigParser to deal with Django environment settings.
    """
    SECTION = 'settings'

    def __init__(self, config_file):
        self.config_file = None
        self.parser = None
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


class ConfigEnv(ConfigBase):
    """
    Handle .env file format used by Foreman.
    """
    _BOOLEANS = {'1': True, 'yes': True, 'true': True, 'on': True,
                 '0': False, 'no': False, 'false': False, 'off': False}

    def __init__(self, config_file):
        self.load(config_file)

    def load(self, config_file):
        """
        Load config data from a file. Taken from jacobian's django-dotenv
        """
        self.config_file = config_file
        self.data = {}

        for line in open(config_file):
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k, v = line.split('=', 1)
            v = v.strip("'").strip('"')
            self.data[k] = v

    def _cast_boolean(self, value):
        """
        Helper to convert config values to boolean as ConfigParser do.
        """
        if value.lower() not in self._BOOLEANS:
            raise ValueError, 'Not a boolean: %s' % v

        return self._BOOLEANS[value.lower()]

    def get(self, option, default=u'', cast=unicode):
        """
        Return the value for option or default option is not defined.
        """
        if cast is bool:
            cast = self._cast_boolean

        if option not in self.data:
            return cast(default)

        return cast(self.data[option])


class AutoConfig(object):
    """
    Autodetects the config file and type.
    """
    SUPPORTED = {
        'settings.ini': ConfigIni,
        '.env': ConfigEnv,
    }

    def __init__(self):
        self.config = None

    def _find_file(self, path):
        # look for all files in the current path
        for filename in self.SUPPORTED:
            file = os.path.join(path, filename)
            if os.path.exists(file):
                return file

        # search the parent
        parent = os.path.dirname(path)
        if parent and parent != os.path.sep:
            return self._find_file(parent)

        # reached root without finding any files.
        return None

    def _load(self, path):
        file = self._find_file(path)

        if not file:
            raise RuntimeError("No supported config file found.")

        klass = self.SUPPORTED.get(os.path.basename(file))
        self.config = klass(file)

    def _caller_path(self):
        # MAGIC! Get the caller's module path.
        frame = sys._getframe()
        path = os.path.dirname(frame.f_back.f_back.f_code.co_filename)
        return path

    def __call__(self, *args, **kwargs):
        if not self.config:
            self._load(self._caller_path())

        return self.config(*args, **kwargs)


# A pré-instantiated AutoConfig to improve decouple's usability
# now just import config and start using with no configuration.
config = AutoConfig()
