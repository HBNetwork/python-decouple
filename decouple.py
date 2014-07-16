# coding: utf-8
import os
import sys
import inspect

# Useful for very coarse version differentiation.
PY3 = sys.version_info[0] == 3

if PY3:
    from configparser import ConfigParser
else:
    from ConfigParser import SafeConfigParser as ConfigParser


class UndefinedValueError(Exception):
    pass


class Undefined(object):
    """
    Class to represent undefined type.
    """
    pass


# Reference instance to represent undefined values
undefined = Undefined()


class Cast(object):
    """
    Class with custom casts
    """

    _BOOLEANS = {
        '1': True, 'yes': True, 'true': True, 'on': True,
        '0': False, 'no': False, 'false': False, 'off': False
    }

    cast = None

    def __init__(self, cast=None):
        if cast:
            self.cast = cast

    def boolean(self, value):
        """
        Helper to convert config values to boolean as ConfigParser do.
        """
        value = str(value)
        if value.lower() not in self._BOOLEANS:
            raise ValueError('Not a boolean: %s' % value)

        return self._BOOLEANS[value.lower()]

    def csv(self, value):
        values = value.split(',')

        if self.cast:
            return [self.cast(v) for v in values]

        return values


class Config(object):

    """
    Handle .env file format used by Foreman.
    """

    def __init__(self, repository):
        self.repository = repository

    def get(self, option, default=undefined, cast=undefined):
        """
        Return the value for option or default if defined.
        """

        value = default
        if option in self.repository:
            value = self.repository.get(option)

        if isinstance(value, Undefined):
            raise UndefinedValueError(
                "{} option not found and default value wasn't defined.".format(
                    option
                )
            )

        if isinstance(cast, Undefined):
            cast = lambda v: v  # nop
        elif cast is bool:
            cast = Cast().boolean

        return cast(value)

    def __call__(self, *args, **kwargs):
        """
        Convenient shortcut to get.
        """
        return self.get(*args, **kwargs)


class RepositoryBase(object):

    def __init__(self, source):
        raise NotImplementedError

    def __contains__(self, key):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError


class RepositoryIni(RepositoryBase):

    """
    Retrieves option keys from .ini files.
    """
    SECTION = 'settings'

    def __init__(self, source):
        self.parser = ConfigParser()
        self.parser.readfp(open(source))

    def __contains__(self, key):
        return self.parser.has_option(self.SECTION, key)

    def get(self, key):
        return self.parser.get(self.SECTION, key)


class RepositoryEnv(RepositoryBase):

    """
    Retrieves option keys from .env files with fall back to os.environ.
    """

    def __init__(self, source):
        self.data = {}

        for line in open(source):
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k, v = line.split('=', 1)
            v = v.strip("'").strip('"')
            self.data[k] = v

    def __contains__(self, key):
        return key in self.data or key in os.environ

    def get(self, key):
        return self.data.get(key) or os.environ[key]


class RepositoryShell(RepositoryBase):

    """
    Retrieves option keys from os.environ.
    """

    def __init__(self, source=None):
        pass

    def __contains__(self, key):
        return key in os.environ

    def get(self, key):
        return os.environ[key]


class AutoConfig(object):

    """
    Autodetects the config file and type.
    """
    SUPPORTED = {
        'settings.ini': RepositoryIni,
        '.env': RepositoryEnv,
    }

    def __init__(self):
        self.config = None

    def _find_file(self, path):
        # look for all files in the current path
        for configfile in self.SUPPORTED:
            filename = os.path.join(path, configfile)
            if os.path.exists(filename):
                return filename

        # search the parent
        parent = os.path.dirname(path)
        if parent and parent != os.path.sep:
            return self._find_file(parent)

        # reached root without finding any files.
        return ''

    def _load(self, path):
        # Avoid unintended permission errors
        try:
            filename = self._find_file(path)
        except Exception:
            filename = ''
        Repository = self.SUPPORTED.get(os.path.basename(filename))

        if not Repository:
            Repository = RepositoryShell

        self.config = Config(Repository(filename))

    def _caller_path(self):
        # MAGIC! Get the caller's module path.
        frame = inspect.currentframe()
        path = os.path.dirname(frame.f_back.f_back.f_code.co_filename)
        return path

    def __call__(self, *args, **kwargs):
        if not self.config:
            self._load(self._caller_path())

        return self.config(*args, **kwargs)


# A pré-instantiated AutoConfig to improve decouple's usability
# now just import config and start using with no configuration.
config = AutoConfig()
