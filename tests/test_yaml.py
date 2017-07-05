# coding: utf-8
import os
import sys
from mock import patch
import pytest
from decouple import Config, RepositoryYaml, UndefinedValueError


# Useful for very coarse version differentiation.
PY3 = sys.version_info[0] == 3

if PY3:
    from io import StringIO
else:
    from StringIO import StringIO


YAMLFILE = '''
KeyTrue: True
KeyOne: 1
KeyYes: yes
KeyOn: on

KeyFalse: False
KeyZero: 0
KeyNo: no
KeyOff: off
KeyEmpty:

KeyList:
    - 1
    - 2
    - 3
    
KeyDict:
    KeyTest: test

#CommentedKey: None
IgnoreSpace: text
RespectSingleQuoteSpace: ' text'
RespectDoubleQuoteSpace: " text"
KeyOverrideByEnv: NotThis
PercentNotEscaped: 90%
'''


@pytest.fixture(scope='module')
def config():
    with patch('decouple.open', return_value=StringIO(YAMLFILE), create=True):
        return Config(RepositoryYaml('settings.yaml'))


def test_env_comment(config):
    with pytest.raises(UndefinedValueError):
        config('CommentedKey')


def test_env_bool_true(config):
    assert True == config('KeyTrue', cast=bool)
    assert True == config('KeyOne', cast=bool)
    assert True == config('KeyYes', cast=bool)
    assert True == config('KeyOn', cast=bool)


def test_env_bool_false(config):
    assert False == config('KeyFalse', cast=bool)
    assert False == config('KeyZero', cast=bool)
    assert False == config('KeyNo', cast=bool)
    assert False == config('KeyOff', cast=bool)


def test_env_os_environ(config):
    os.environ['KeyOverrideByEnv'] = 'This'
    assert 'This' == config('KeyOverrideByEnv')
    del os.environ['KeyOverrideByEnv']


def test_env_undefined(config):
    with pytest.raises(UndefinedValueError):
        config('UndefinedKey')


def test_env_default_none(config):
    assert None is config('UndefinedKey', default=None)


def test_env_empty(config):
    assert None is config('KeyEmpty', default=None)


def test_env_support_space(config):
    assert 'text' == config('IgnoreSpace')
    assert ' text' == config('RespectSingleQuoteSpace')
    assert ' text' == config('RespectDoubleQuoteSpace')


def test_list_as_list(config):
    assert isinstance(config('KeyList'), list)


def test_dict_as_dict(config):
    assert isinstance(config('KeyDict'), dict)


def test_env_percent_not_escaped(config):
    assert '90%' == config('PercentNotEscaped')