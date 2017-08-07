# coding: utf-8
import os
import sys
from mock import patch
import pytest
from decouple import Config, RepositoryEnv, UndefinedValueError


# Useful for very coarse version differentiation.
PY3 = sys.version_info[0] == 3

if PY3:
    from io import StringIO
else:
    from io import BytesIO as StringIO


ENVFILE = '''
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
PercentNotEscaped=%%
NoInterpolation=%(KeyOff)s
IgnoreSpace = text
RespectSingleQuoteSpace = ' text'
RespectDoubleQuoteSpace = " text"
KeyOverrideByEnv=NotThis
'''

@pytest.fixture(scope='module')
def config():
    with patch('decouple.open', return_value=StringIO(ENVFILE), create=True):
        return Config(RepositoryEnv('.env'))


def test_env_comment(config):
    with pytest.raises(UndefinedValueError):
        config('CommentedKey')


def test_env_percent_not_escaped(config):
    assert '%%' == config('PercentNotEscaped')


def test_env_no_interpolation(config):
    assert '%(KeyOff)s' == config('NoInterpolation')


def test_env_bool_true(config):
    assert True is config('KeyTrue', cast=bool)
    assert True is config('KeyOne', cast=bool)
    assert True is config('KeyYes', cast=bool)
    assert True is config('KeyOn', cast=bool)


def test_env_bool_false(config):
    assert False is config('KeyFalse', cast=bool)
    assert False is config('KeyZero', cast=bool)
    assert False is config('KeyNo', cast=bool)
    assert False is config('KeyOff', cast=bool)


def test_env_os_environ(config):
    os.environ['KeyOverrideByEnv'] = 'This'
    assert 'This' == config('KeyOverrideByEnv')
    del os.environ['KeyOverrideByEnv']


def test_env_undefined_but_present_in_os_environ(config):
    os.environ['KeyOnlyEnviron'] = ''
    assert '' == config('KeyOnlyEnviron')
    del os.environ['KeyOnlyEnviron']


def test_env_undefined(config):
    with pytest.raises(UndefinedValueError):
        config('UndefinedKey')


def test_env_default_none(config):
    assert None is config('UndefinedKey', default=None)


def test_env_empty(config):
    assert '' == config('KeyEmpty', default=None)
    assert '' == config('KeyEmpty')


def test_env_support_space(config):
    assert 'text' == config('IgnoreSpace')
    assert ' text' == config('RespectSingleQuoteSpace')
    assert ' text' == config('RespectDoubleQuoteSpace')


def test_env_empty_string_means_false(config):
    assert False is config('KeyEmpty', cast=bool)
