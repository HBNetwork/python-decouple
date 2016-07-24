# coding: utf-8
import os
import pytest
from mock import patch
from decouple import AutoConfig


def test_manualconfig_env():
    path_config = os.path.join(os.path.dirname(__file__), 'autoconfig', 'env', 'project')
    config = AutoConfig(path_config)
    assert 'ENV' == config('KEY')


def test_manualconfig_ini():
    path_config = os.path.join(os.path.dirname(__file__), 'autoconfig', 'ini', 'project')
    config = AutoConfig(path_config)
    assert 'INI' == config('KEY')


def test_manualconfig_none():
    os.environ['KeyFallback'] = 'On'
    path_config = os.path.join(os.path.dirname(__file__), 'autoconfig', 'none')
    config = AutoConfig(path_config)
    assert True == config('KeyFallback', cast=bool)
    del os.environ['KeyFallback']

