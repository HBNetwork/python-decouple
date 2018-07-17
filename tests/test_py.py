# coding: utf-8
import sys
import pytest
from decouple import Config, RepositoryPython, UndefinedValueError


# Useful for very coarse version differentiation.
PY3 = sys.version_info[0] == 3

if PY3:
    from io import StringIO
else:
    from io import BytesIO as StringIO


@pytest.fixture(scope='module')
def config():
    return Config(RepositoryPython('tests/config/config.py'))


def test_python_comment(config):
    with pytest.raises(UndefinedValueError):
        config('CommentedKey')


def test_python_percent_not_escaped(config):
    assert '%%' == config('PercentNotEscaped')


def test_python_no_interpolation(config):
    assert '%(KeyOff)s' == config('NoInterpolation')


def test_python_bool_true(config):
    assert True is config('KeyTrue', cast=bool)
    assert True is config('KeyOne', cast=bool)
    assert True is config('KeyYes', cast=bool)
    assert True is config('KeyOn', cast=bool)


def test_python_bool_false(config):
    assert False is config('KeyFalse', cast=bool)
    assert False is config('KeyZero', cast=bool)
    assert False is config('KeyNo', cast=bool)
    assert False is config('KeyOff', cast=bool)


def test_python_default_none(config):
    assert None is config('UndefinedKey', default=None)


def test_python_empty(config):
    assert '' == config('KeyEmpty', default=None)
    assert '' == config('KeyEmpty')


def test_python_support_space(config):
    assert 'text' == config('IgnoreSpace')
    # assert ' text' == config('RespectSingleQuoteSpace')
    assert ' text' == config('RespectDoubleQuoteSpace')


def test_python_empty_string_means_false(config):
    assert False is config('KeyEmpty', cast=bool)


def test_python_none_means_false(config):
    assert False is config('KeyNone', cast=bool)
