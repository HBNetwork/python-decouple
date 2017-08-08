# coding: utf-8
import os
import sys
from mock import patch, mock_open
import pytest
from decouple import Config, RepositoryJSON, UndefinedValueError

# Useful for very coarse version differentiation.
PY3 = sys.version_info[0] == 3

if PY3:
    from io import StringIO
else:
    from StringIO import StringIO


JSONFILE = '''
{
    "KeyTrue": true,
    "KeyOne": 1,
    "KeyFalse": false,
    "KeyZero": 0,
    "KeyEmpty": null,
    "PercentIsEscaped": "%%",
    "Interpolation": "%(KeyOff)s",
    "KeyOverrideByEnv": "NotThis"
}
'''


@pytest.fixture(scope='module')
def config():
    with patch('decouple.open', return_value=StringIO(JSONFILE), create=True):
        return Config(RepositoryJSON('settings.json'))


def test_json_bool_true(config):
    print(config('KeyTrue', cast=bool))
    
    assert config('KeyTrue', cast=bool)
    assert config('KeyOne', cast=bool)


def test_json_bool_false(config):
    assert not config('KeyFalse', cast=bool)
    assert not config('KeyZero', cast=bool)


def test_json_percent_escape(config):
    assert '%' == config('PercentIsEscaped')


def test_jsont_undefined(config):
    with pytest.raises(UndefinedValueError):
        config('UndefinedKey')


def test_json_default_none(config):
    assert None is config('UndefinedKey', default=None)


def test_json_default_bool(config):
    assert not config('UndefinedKey', default=False, cast=bool)
    assert config('UndefinedKey', default=True, cast=bool)


def test_json_default(config):
    assert not config('UndefinedKey', default=False)
    assert config('UndefinedKey', default=True)


def test_json_default_invalid_bool(config):
    with pytest.raises(ValueError):
        config('UndefinedKey', default='NotBool', cast=bool)


def test_json_os_environ(config):
    os.environ['KeyOverrideByEnv'] = 'This'
    assert 'This' == config('KeyOverrideByEnv')
    del os.environ['KeyOverrideByEnv']
