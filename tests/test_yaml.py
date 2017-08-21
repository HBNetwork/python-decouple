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
    from io import BytesIO as StringIO


YAMLFILE = '''
settings:
    KeyTrue: true
    KeyOne: 1
    KeyYes: yes
    KeyOn: on

    KeyFalse: false
    KeyZero: 0
    KeyNo: no
    KeyOff: off
    KeyEmpty: ''

    #CommentedKey: None
    IgnoreSpace:  text
    RespectSingleQuoteSpace :  ' text'
    RespectDoubleQuoteSpace :  " text"
    KeyOverrideByEnv: NotThis

    List:
        - Item1
        - Item2
        - Item3

    Repeat: &id1
        Node1: 1
        Node2: 2

    RepeatedNode: *id1
    ChangeNode:
        <<: *id1
        Node2: 3
'''


@pytest.fixture(scope='module')
def config():
    with patch('decouple.open', return_value=StringIO(YAMLFILE), create=True):
        return Config(RepositoryYaml('settings.yaml'))


def test_yaml_comment(config):
    with pytest.raises(UndefinedValueError):
        config('CommentedKey')


def test_yaml_bool_true(config):
    assert True is config('KeyTrue', cast=bool)
    assert True is config('KeyOne', cast=bool)
    assert True is config('KeyYes', cast=bool)
    assert True is config('KeyOn', cast=bool)


def test_yaml_bool_false(config):
    assert False is config('KeyFalse', cast=bool)
    assert False is config('KeyZero', cast=bool)
    assert False is config('KeyNo', cast=bool)
    assert False is config('KeyOff', cast=bool)


def test_yaml_os_environ(config):
    os.environ['KeyOverrideByEnv'] = 'This'
    assert 'This' == config('KeyOverrideByEnv')
    del os.environ['KeyOverrideByEnv']


def test_yaml_undefined_but_present_in_os_environ(config):
    os.environ['KeyOnlyEnviron'] = ''
    assert '' == config('KeyOnlyEnviron')
    del os.environ['KeyOnlyEnviron']


def test_yaml_undefined(config):
    with pytest.raises(UndefinedValueError):
        config('UndefinedKey')


def test_yaml_default_none(config):
    assert None is config('UndefinedKey', default=None)


def test_yaml_empty(config):
    assert '' == config('KeyEmpty', default=None)
    assert '' == config('KeyEmpty')


def test_yaml_support_space(config):
    assert 'text' == config('IgnoreSpace')
    assert ' text' == config('RespectSingleQuoteSpace')
    assert ' text' == config('RespectDoubleQuoteSpace')


def test_yaml_empty_string_means_false(config):
    assert False is config('KeyEmpty', cast=bool)


def test_yaml_list(config):
    assert isinstance(config('List'), list)
    assert len(config('List')) == 3


def test_yaml_repeated_node(config):
    assert config('RepeatedNode')['Node1'] == 1
    assert config('RepeatedNode')['Node2'] == 2

    assert config('ChangeNode')['Node2'] == 3
