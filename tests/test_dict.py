# coding: utf-8
import sys
from mock import patch
import pytest
from decouple import Config, RepositoryDict, UndefinedValueError


# Useful for very coarse version differentiation.
PY3 = sys.version_info[0] == 3

if PY3:
    from io import StringIO
else:
    from io import BytesIO as StringIO


DICTFILE = dict(
    KeyTrue=True,
    KeyOne=1,
    KeyYes='yes',
    KeyOn='on',

    KeyFalse=False,
    KeyZero=0,
    KeyNo='no',
    KeyOff='off',
    KeyEmpty='',
    KeyNone=None,

    #CommentedKey=None
    PercentNotEscaped='%%',
    NoInterpolation='%(KeyOff)s',
    IgnoreSpace = 'text',
    RespectSingleQuoteSpace = ' text',
    RespectDoubleQuoteSpace = " text",
    KeyOverrideByEnv='NotThis',

    KeyBool = True,
    KeyList = [1,2],
)


@pytest.fixture(scope='module')
def config():
    return Config(RepositoryDict(DICTFILE))


def test_dict_comment(config):
    with pytest.raises(UndefinedValueError):
        config('CommentedKey')


def test_dict_percent_not_escaped(config):
    assert '%%' == config('PercentNotEscaped')


def test_dict_no_interpolation(config):
    assert '%(KeyOff)s' == config('NoInterpolation')


def test_dict_bool_true(config):
    assert True is config('KeyTrue', cast=bool)
    assert True is config('KeyOne', cast=bool)
    assert True is config('KeyYes', cast=bool)
    assert True is config('KeyOn', cast=bool)


def test_dict_bool_false(config):
    assert False is config('KeyFalse', cast=bool)
    assert False is config('KeyZero', cast=bool)
    assert False is config('KeyNo', cast=bool)
    assert False is config('KeyOff', cast=bool)


def test_dict_default_none(config):
    assert None is config('UndefinedKey', default=None)


def test_dict_empty(config):
    assert '' == config('KeyEmpty', default=None)
    assert '' == config('KeyEmpty')


def test_dict_support_space(config):
    assert 'text' == config('IgnoreSpace')
    # assert ' text' == config('RespectSingleQuoteSpace')
    assert ' text' == config('RespectDoubleQuoteSpace')


def test_dict_empty_string_means_false(config):
    assert False is config('KeyEmpty', cast=bool)


def test_dict_cast_not_required(config):
    assert True is config('KeyBool')


def test_dict_cast_structured_type(config):
    assert [1,2] == config('KeyList')
