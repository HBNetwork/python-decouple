# coding: utf-8
import os
import pytest
from mock import patch
from decouple import AutoConfig, UndefinedValueError, RepositoryEmpty


def test_autoconfig_env():
    config = AutoConfig()
    path = os.path.join(os.path.dirname(__file__), 'autoconfig', 'env', 'project')
    with patch.object(config, '_caller_path', return_value=path):
        assert 'ENV' == config('KEY')


def test_autoconfig_ini():
    config = AutoConfig()
    path = os.path.join(os.path.dirname(__file__), 'autoconfig', 'ini', 'project')
    with patch.object(config, '_caller_path', return_value=path):
        assert 'INI' == config('KEY')


def test_autoconfig_ini_in_subdir():
    """
    When `AutoConfig._find_file()` gets a relative path from
    `AutoConfig._caller_path()`, it will not properly search back to parent
    dirs.

    This is a regression test to make sure that when
    `AutoConfig._caller_path()` finds something like `./config.py` it will look
    for settings.ini in parent directories.
    """
    config = AutoConfig()
    subdir = os.path.join(os.path.dirname(__file__), 'autoconfig', 'ini',
            'project', 'subdir')
    os.chdir(subdir)
    path = os.path.join(os.path.curdir, 'empty.py')
    with patch.object(config, '_caller_path', return_value=path):
        assert 'INI' == config('KEY')


def test_autoconfig_none():
    os.environ['KeyFallback'] = 'On'
    config = AutoConfig()
    with patch('os.path.isfile', return_value=False):
        assert True is config('KeyFallback', cast=bool)
    del os.environ['KeyFallback']


def test_autoconfig_exception():
    os.environ['KeyFallback'] = 'On'
    config = AutoConfig()
    with patch('os.path.isfile', side_effect=Exception('PermissionDenied')):
        assert True is config('KeyFallback', cast=bool)
    del os.environ['KeyFallback']


def test_autoconfig_is_not_a_file():
    os.environ['KeyFallback'] = 'On'
    config = AutoConfig()
    with patch('os.path.isfile', return_value=False):
        assert True is config('KeyFallback', cast=bool)
    del os.environ['KeyFallback']


def test_env_os_environ():
    os.environ['KeyOverrideByEnv'] = 'This'
    config = AutoConfig()
    assert 'This' == config('KeyOverrideByEnv')
    del os.environ['KeyOverrideByEnv']


def test_env_undefined_but_present_in_os_environ():
    os.environ['KeyOnlyEnviron'] = ''
    config = AutoConfig()
    assert '' == config('KeyOnlyEnviron')
    del os.environ['KeyOnlyEnviron']


def test_env_undefined():
    config = AutoConfig()
    with pytest.raises(UndefinedValueError):
        config('UndefinedKey')


def test_autoconfig_search_path():
    path = os.path.join(os.path.dirname(__file__), 'autoconfig', 'env', 'custom-path')
    config = AutoConfig(path)
    assert 'CUSTOMPATH' == config('KEY')


def test_autoconfig_empty_repository():
    path = os.path.join(os.path.dirname(__file__), 'autoconfig', 'env', 'custom-path')
    config = AutoConfig(path)

    with pytest.raises(UndefinedValueError):
        config('KeyNotInEnvAndNotInRepository')

    assert isinstance(config.config.repository, RepositoryEmpty)
