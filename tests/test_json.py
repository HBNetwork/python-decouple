# coding: utf-8
import sys
from mock import patch
import pytest
from decouple import Config, RepositoryJSON, UndefinedValueError


# Useful for very coarse version differentiation.
PY3 = sys.version_info[0] == 3

if PY3:
    from io import StringIO
else:
    from io import BytesIO as StringIO


JSONFILE = '''
{
    "KeyTrue":true,
    "KeyOne":1,
    "KeyYes":"yes",
    "KeyOn":"on",

    "KeyFalse":false,
    "KeyZero":0,
    "KeyNo":"no",
    "KeyOff":"off",
    "KeyEmpty":"",

    "PercentNotEscaped":"%%",
    "NoInterpolation":"%(KeyOff)s",
    "IgnoreSpace" : "text",
    "RespectDoubleQuoteSpace" : " text",
    "KeyOverrideByEnv":"NotThis"
}
'''


@pytest.fixture(scope='module')
def config():
    with patch('decouple.open', return_value=StringIO(JSONFILE), create=True):
        with patch('decouple.os.path.isfile', return_value=True):
            return Config(RepositoryJSON('settings.json'))


def test_json_comment(config):
    with pytest.raises(UndefinedValueError):
        config('CommentedKey')


def test_json_percent_not_escaped(config):
    assert '%%' == config('PercentNotEscaped')


def test_json_no_interpolation(config):
    assert '%(KeyOff)s' == config('NoInterpolation')


def test_json_bool_true(config):
    assert True is config('KeyTrue', cast=bool)
    assert True is config('KeyOne', cast=bool)
    assert True is config('KeyYes', cast=bool)
    assert True is config('KeyOn', cast=bool)


def test_json_bool_false(config):
    assert False is config('KeyFalse', cast=bool)
    assert False is config('KeyZero', cast=bool)
    assert False is config('KeyNo', cast=bool)
    assert False is config('KeyOff', cast=bool)


def test_json_default_none(config):
    assert None is config('UndefinedKey', default=None)


def test_json_empty(config):
    assert '' == config('KeyEmpty', default=None)
    assert '' == config('KeyEmpty')


def test_json_support_space(config):
    assert 'text' == config('IgnoreSpace')
    # assert ' text' == config('RespectSingleQuoteSpace')
    assert ' text' == config('RespectDoubleQuoteSpace')


def test_json_empty_string_means_false(config):
    assert False is config('KeyEmpty', cast=bool)
