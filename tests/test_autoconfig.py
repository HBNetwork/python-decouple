# coding: utf-8
import os
import pytest
from mock import patch
from decouple import AutoConfig


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
    path = os.path.join(os.path.dirname(__file__), 'autoconfig', 'none')
    with patch('os.path.isfile', return_value=False):
        assert True == config('KeyFallback', cast=bool)
    del os.environ['KeyFallback']


def test_autoconfig_exception():
    os.environ['KeyFallback'] = 'On'
    config = AutoConfig()
    with patch('os.path.isfile', side_effect=Exception('PermissionDenied')):
        assert True == config('KeyFallback', cast=bool)
    del os.environ['KeyFallback']


def test_autoconfig_is_not_a_file():
    os.environ['KeyFallback'] = 'On'
    config = AutoConfig()
    with patch('os.path.isfile', return_value=False):
        assert True == config('KeyFallback', cast=bool)
    del os.environ['KeyFallback']
