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
    from StringIO import StringIO



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
    assert True == config('KeyTrue', cast=bool)
    assert True == config('KeyOne', cast=bool)
    assert True == config('KeyYes', cast=bool)
    assert True == config('KeyOn', cast=bool)

def test_ini_bool_false(config):
    assert False == config('KeyFalse', cast=bool)
    assert False == config('KeyZero', cast=bool)
    assert False == config('KeyNo', cast=bool)
    assert False == config('KeyOff', cast=bool)

def test_init_undefined(config):
    with pytest.raises(UndefinedValueError):
        config('UndefinedKey')

def test_ini_default_none(config):
    assert None is config('UndefinedKey', default=None)

def test_ini_default_bool(config):
    assert False == config('UndefinedKey', default=False, cast=bool)
    assert True == config('UndefinedKey', default=True, cast=bool)

def test_ini_default(config):
    assert False == config('UndefinedKey', default=False)
    assert True == config('UndefinedKey', default=True)

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
