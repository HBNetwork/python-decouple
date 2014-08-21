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
    from StringIO import StringIO


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
KeyEmptyWithComments=  # no comments

#CommentedKey=None
InvalidKey#Skipped
InlineComments=Foo  # This is an inline comment
HashContent=Foo 'Bar # Baz' %(key)s  # This is an inline comment
PercentNotEscaped=%%
NoInterpolation=%(KeyOff)s
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
    os.environ['KeyFallback'] = 'On'
    assert True == config('KeyTrue', cast=bool)
    assert True == config('KeyFallback', cast=bool)
    del os.environ['KeyFallback']

def test_env_undefined(config):
    with pytest.raises(UndefinedValueError):
        config('UndefinedKey')

def test_env_default_none(config):
    assert None is config('UndefinedKey', default=None)

def test_env_empty(config):
    assert '' is config('KeyEmpty', default=None)

def test_env_empty_with_comments(config):
    assert '' is config('KeyEmptyWithComments', default=None)

def test_env_inline_comment(config):
    assert 'Foo' == config("InlineComments")

def test_env_inline_comment_with_hash_in_value(config):
    assert "Foo 'Bar # Baz' %(key)s" == config("HashContent")

def test_env_undefined_for_invalid_key(config):
    with pytest.raises(UndefinedValueError):
        config('InvalidKey')
