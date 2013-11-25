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


def test_autoconfig_none():
    os.environ['KeyFallback'] = 'On'
    config = AutoConfig()
    path = os.path.join(os.path.dirname(__file__), 'autoconfig', 'none')
    with patch('os.path.exists', return_value=False):
        assert True == config('KeyFallback', cast=bool)
    del os.environ['KeyFallback']


def test_autoconfig_exception():
    os.environ['KeyFallback'] = 'On'
    config = AutoConfig()
    with patch('os.path.exists', side_effect=Exception('PermissionDenied')):
        assert True == config('KeyFallback', cast=bool)
    del os.environ['KeyFallback']
