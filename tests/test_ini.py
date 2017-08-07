# coding: utf-8
import os
import sys
from mock import patch, mock_open
import pytest
from decouple import Config, RepositoryIni, UndefinedValueError

# Useful for very coarse version differentiation.
PY3 = sys.version_info[0] == 3

if PY3:
    from io import StringIO
else:
    from io import BytesIO as StringIO



INIFILE = '''
[settings]
KeyTrue=True
KeyOne=1
KeyYes=yes
KeyOn=on

KeyFalse=False
KeyZero=0
KeyNo=no
KeyOff=off
KeyEmpty=

#CommentedKey=None
PercentIsEscaped=%%
Interpolation=%(KeyOff)s
IgnoreSpace = text
KeyOverrideByEnv=NotThis
'''

@pytest.fixture(scope='module')
def config():
    with patch('decouple.open', return_value=StringIO(INIFILE), create=True):
        return Config(RepositoryIni('settings.ini'))


def test_ini_comment(config):
    with pytest.raises(UndefinedValueError):
        config('CommentedKey')


def test_ini_percent_escape(config):
    assert '%' == config('PercentIsEscaped')


def test_ini_interpolation(config):
    assert 'off' == config('Interpolation')


def test_ini_bool_true(config):
    assert True is config('KeyTrue', cast=bool)
    assert True is config('KeyOne', cast=bool)
    assert True is config('KeyYes', cast=bool)
    assert True is config('KeyOn', cast=bool)


def test_ini_bool_false(config):
    assert False is config('KeyFalse', cast=bool)
    assert False is config('KeyZero', cast=bool)
    assert False is config('KeyNo', cast=bool)
    assert False is config('KeyOff', cast=bool)


def test_init_undefined(config):
    with pytest.raises(UndefinedValueError):
        config('UndefinedKey')


def test_ini_default_none(config):
    assert None is config('UndefinedKey', default=None)


def test_ini_default_bool(config):
    assert False is config('UndefinedKey', default=False, cast=bool)
    assert True is config('UndefinedKey', default=True, cast=bool)


def test_ini_default(config):
    assert False is config('UndefinedKey', default=False)
    assert True is config('UndefinedKey', default=True)


def test_ini_default_invalid_bool(config):
    with pytest.raises(ValueError):
        config('UndefinedKey', default='NotBool', cast=bool)


def test_ini_empty(config):
    assert '' is config('KeyEmpty', default=None)


def test_ini_support_space(config):
    assert 'text' == config('IgnoreSpace')


def test_ini_os_environ(config):
    os.environ['KeyOverrideByEnv'] = 'This'
    assert 'This' == config('KeyOverrideByEnv')
    del os.environ['KeyOverrideByEnv']


def test_ini_undefined_but_present_in_os_environ(config):
    os.environ['KeyOnlyEnviron'] = ''
    assert '' == config('KeyOnlyEnviron')
    del os.environ['KeyOnlyEnviron']


def test_ini_empty_string_means_false(config):
    assert False is config('KeyEmpty', cast=bool)
