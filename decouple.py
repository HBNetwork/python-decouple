# coding: utf-8
import os
import sys
import string
from shlex import shlex


# Useful for very coarse version differentiation.
PY3 = sys.version_info[0] == 3

if PY3:
    from configparser import ConfigParser
    text_type = str
else:
    from ConfigParser import SafeConfigParser as ConfigParser
    text_type = unicode

class DoesNotExist(Exception):
    pass


class UndefinedValueError(Exception):
    pass


class UnsupportedExtensionError(Exception):
    pass


class UnsupportedFormatError(Exception):
    pass


class Undefined(object):
    """
    Class to represent undefined type.
    """
    pass


# Reference instance to represent undefined values
undefined = Undefined()


class Config(object):
    """
    Handle option retrieval with default and casting.
    """
    _BOOLEANS = {'1': True, 'yes': True, 'true': True, 'on': True,
                 '0': False, 'no': False, 'false': False, 'off': False, '': False}

    def __init__(self, repository):
        self.repository = repository

    def _cast_boolean(self, value):
        """
        Helper to convert config values to boolean as ConfigParser do.
        """
        if isinstance(value, bool):
            return value
        elif value is None:
            return False

        value = str(value)
        if value.lower() not in self._BOOLEANS:
            raise ValueError('Not a boolean: %s' % value)

        return self._BOOLEANS[value.lower()]

    @staticmethod
    def _cast_do_nothing(value):
        return value

    def __contains__(self, option):
        return option in self.repository

    def get(self, option, default=undefined, cast=undefined):
        """
        Return the value for option or default if defined.
        """

        # We can't avoid __contains__ because value may be empty.
        if option in self.repository:
            value = self.repository[option]
        else:
            if isinstance(default, Undefined):
                raise UndefinedValueError('{} not found. Declare it as envvar or define a default value.'.format(option))

            value = default

        if isinstance(cast, Undefined):
            cast = self._cast_do_nothing
        elif cast is bool:
            cast = self._cast_boolean

        return cast(value)

    def __call__(self, *args, **kwargs):
        """
        Convenient shortcut to get.
        """
        return self.get(*args, **kwargs)


# A Repository base class that acts like an empty repository
class RepositoryEmpty(object):
    def __init__(self, source=''):
        pass

    def __contains__(self, key):
        return False

    def __getitem__(self, key):
        return None


class RepositoryOS(RepositoryEmpty):
    """
    Retrieves option keys from os environment.
    """
    def __init__(self, source=None):
        pass

    def __contains__(self, key):
        return key in os.environ

    def __getitem__(self, key):
        return os.environ.get(key)

    def dict(self):
        return os.environ


class RepositoryIni(RepositoryEmpty):
    """
    Retrieves option keys from a .ini file.
    """
    SECTION = 'settings'

    def __init__(self, source):
        if not os.path.isfile(source):
            raise DoesNotExist('Config file "{}" not found'.format(source))
        self.parser = ConfigParser()
        with open(source) as file_:
            self.parser.readfp(file_)

    def __contains__(self, key):
        return self.parser.has_option(self.SECTION, key)

    def __getitem__(self, key):
        return self.parser.get(self.SECTION, key)

    def dict(self):
        # NOTE: According to https://docs.python.org/2/library/configparser.html:
        #   The default ConfigParser implementation converts option names to lower case.
        return {option: self[option] for option in self.parser.options(self.SECTION)}


class RepositoryEnv(RepositoryEmpty):
    """
    Retrieves option keys from a .env file.
    """
    def __init__(self, source):
        self.data = {}

        if not os.path.isfile(source):
            raise DoesNotExist('Config file "{}" not found'.format(source))

        with open(source) as file_:
            for line in file_:
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                k, v = line.split('=', 1)
                k = k.strip()
                v = v.strip().strip('\'"')
                self.data[k] = v

    def __contains__(self, key):
        return key in self.data

    def __getitem__(self, key):
        return self.data[key]

    def dict(self):
        return self.data


class RepositoryPython(RepositoryEmpty):
    """
    Retrieves option keys from a python module.
    All globals not beginning with '_' are treated as option keys.

    It's up to the caller to make sure that the 
    specified file is on the PYTHON_PATH.

    This type of repository has these advantages:
    1) Casting is unnecessary, since the settings have a type.
    2) Settings can be structured types like lists or dicts.
    3) Settings files use all the same syntax and features
       that Python programmers are used to.
    And these disadvantages:
    1) A single error in the file will prevent the whole file from loading.
    2) It must be importable by python
       (among other things, this means it must be on the PYTHON_PATH).
    """
    def __init__(self, source):
        self.data = {}

        # Build python module name from directory names and file name minus extension
        dir_name = os.path.dirname(source).replace('\\', '/')
        file_name, file_extension = os.path.basename(source).split('.')
        module_parts = dir_name.split('/') if dir_name else []
        module_parts.append(file_name)
        module_name = '.'.join(module_parts)

        from importlib import import_module
        try:
            settings = import_module(module_name)
        except ImportError:
            raise DoesNotExist('Config file "{}" not found'.format(source))
        iter = settings.__dict__.items() if PY3 else settings.__dict__.iteritems()
        for k, v in iter:
            if not k.startswith('_'):
                self.data[k] = v

    def __contains__(self, key):
        return key in self.data

    def __getitem__(self, key):
        return self.data[key]

    def dict(self):
        return self.data


class RepositoryJSON(RepositoryEmpty):
    """
    Retrieves option keys from a JSON file.
    The file, when loaded, is assumed to return a python dict,
    the keys of which are used as option keys.

    This type of repository has these advantages:
    1) Casting is unnecessary, since the settings have a type.
    2) Settings can be structured types like lists or dicts.
    And these disadvantages:
    1) A single error in the file will prevent the whole file from loading.
    2) It's trickier than any of the other formats to edit manually.
    """
    def __init__(self, source):
        if not os.path.isfile(source):
            raise DoesNotExist('Config file "{}" not found'.format(source))

        import json
        with open(source) as file_:
            self.data = json.load(file_)
            if not isinstance(self.data, dict):
                raise UnsupportedFormatError("The JSON file {} didn't return a dict when loaded".format(source))

    def __contains__(self, key):
        return key in self.data

    def __getitem__(self, key):
        return self.data[key]

    def dict(self):
        return self.data


class RepositoryDict(RepositoryEmpty):
    def __init__(self, source=None):
        self.data = source or dict()

    def update(self, dct):
        self.data.update(dct)

    def __contains__(self, key):
        return key in self.data

    def __getitem__(self, key):
        return self.data[key]

    def dict(self):
        return self.data


# NOTE: .ini files are intentionally omitted.
# They don't mix well with the other formats because,
# unlike the other formats, they use case-insensitive keys.
# If you want to use them anyway, simply add them youself,
# e.g. like this:
# import decouple
# config = decouple.MultiConfig(...)
# config.supported_extensions['ini'] = decouple.RepositoryIni
SUPPORTED_EXTENSIONS = {
    'os': RepositoryOS,
    'env': RepositoryEnv,
    'py': RepositoryPython,
    'json': RepositoryJSON,
}


class AutoConfig(object):
    """
    Autodetects the config file and type.

    Parameters
    ----------
    search_path : str, optional
        Initial search path. If empty, the default search path is the
        caller's path.

    """
    SUPPORTED = {
        'settings.ini': RepositoryIni,
        '.env': RepositoryEnv,
    }

    def __init__(self, search_path=None):
        self.search_path = search_path
        self.environ_config = Config(RepositoryOS())
        self.config = None

    def _find_file(self, path):
        # look for all files in the current path
        for configfile in self.SUPPORTED:
            filename = os.path.join(path, configfile)
            if os.path.isfile(filename):
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
            filename = self._find_file(os.path.abspath(path))
        except Exception:
            filename = ''
        Repository = self.SUPPORTED.get(os.path.basename(filename), RepositoryEmpty)

        self.config = Config(Repository(filename))

    def _caller_path(self):
        # MAGIC! Get the caller's module path.
        frame = sys._getframe()
        path = os.path.dirname(frame.f_back.f_back.f_code.co_filename)
        return path

    def __call__(self, option, *args, **kwargs):
        if not self.config:
            self._load(self.search_path or self._caller_path())

        if option in self.environ_config:
            return self.environ_config(option, *args, **kwargs)
        else:
            return self.config(option, *args, **kwargs)


class MultiConfig(object):
    """
    Loads settings from multiple config files.
    This allows settings of different types to be separated into different files.
    Settings in earlier files override settings in later files.

    For python files, the caller is responsible for ensuring that the
    file is accessible from the PYTHON_PATH.
    
    For other files, the caller should pass either a relative path that
    is accessible from the current directory, or a full path.

    Note that MulticConfig does not check os environment variables unless '.os'
    is included in the list of config 'files'. Its precedence is
    specified by its position in the list, just as for other configs.

    Parameters
    ----------
    Config file names OR pre-loaded repository objects

    Example
    -------
    config = MultiConfig('.os', 'envs/config.py', 'envs/secrets.env')
    # This will look for settings:
    # 1) First in an environment variable ('.os')
    # 2) Then in the python module env.config (for general settings)
    # 3) Then in the file envs/secrets.env (for passwords, etc.)

    More complex example
    -------------------
    defaults = {'default1':'value1', 'default2':'value2'}
    config = MultiConfig('.os', 'envs/site.env')
    SITE_TYPE = config('SITE_TYPE')
    config = MultiConfig('.os', 'envs/site.env', 'config_{}.py'.format(SITE_TYPE), 'envs/secrets.env', RepositoryDict(defaults))
    # This first determines the site type (e.g. 'production', 'staging', 'development')
    # from an environment variable or the config file envs/site.env.
    # It then loads an additional config file based on that site type.
    # Mostly likely, the config file based on the site type would be under
    # source control, while site.env and secrets.env would not be.
    # Note the use of a pre-loaded dictionary repository for defaults.
    """

    def __init__(self, *args):
        super(MultiConfig, self).__init__()
        self._env_files = args
        self._configs = None
        self.combine_settings = True
        self.supported_extensions = SUPPORTED_EXTENSIONS.copy()
    
    def _load(self):
        repositories = []
        for config_file in self._env_files:
            if isinstance(config_file, RepositoryEmpty):
                repository = config_file
            else:
                file_extension = config_file.split('.')[-1]
                RepositoryType = self.supported_extensions.get(file_extension, None)
                if RepositoryType is None:
                    raise UnsupportedExtensionError('Config file {} has unsupported extension .{}'.format(config_file, file_extension))
                repository = RepositoryType(config_file)
            repositories.append(repository)
        
        if self.combine_settings:
            repositories.reverse()
            combined_repository = RepositoryDict()
            for repository in repositories:
                combined_repository.update(repository.dict())
            repositories = [combined_repository]

        self._configs = [Config(repository) for repository in repositories]

    def __call__(self, option, *args, **kwargs):
        if self._configs is None:
            self._load()

        for config in self._configs:
            try:
                return config(option, *args, **kwargs)
            except Exception as x:
                pass
        else:
            raise x


# A pre-instantiated AutoConfig to improve decouple's usability
# now just import config and start using with no configuration.
config = AutoConfig()


# Helpers

class Csv(object):
    """
    Produces a csv parser that return a list of transformed elements.
    """

    def __init__(self, cast=text_type, delimiter=',', strip=string.whitespace, post_process=list):
        """
        Parameters:
        cast -- callable that transforms the item just before it's added to the list.
        delimiter -- string of delimiters chars passed to shlex.
        strip -- string of non-relevant characters to be passed to str.strip after the split.
        tuple_ -- boolean to check if it is to return in tuple format.
        """
        self.cast = cast
        self.delimiter = delimiter
        self.strip = strip
        self.post_process = post_process

    def __call__(self, value):
        """The actual transformation"""
        transform = lambda s: self.cast(s.strip(self.strip))

        splitter = shlex(value, posix=True)
        splitter.whitespace = self.delimiter
        splitter.whitespace_split = True

        return self.post_process(transform(s) for s in splitter)
