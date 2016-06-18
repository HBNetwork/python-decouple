# coding: utf-8
import os
import pytest
from mock import patch
from decouple import AutoConfig


def test_manualconfig_env():
    config = AutoConfig()
    path = os.path.join(os.path.dirname(__file__), 'autoconfig', 'env', 'project')
    config.set_config_dir(path)
    assert 'ENV' == config('KEY')


def test_manualconfig_ini():
    config = AutoConfig()
    path = os.path.join(os.path.dirname(__file__), 'autoconfig', 'ini', 'project')
    config.set_config_dir(path)
    assert 'INI' == config('KEY')


def test_manualconfig_none():
    os.environ['KeyFallback'] = 'On'
    config = AutoConfig()
    path = os.path.join(os.path.dirname(__file__), 'autoconfig', 'none')
    config.set_config_dir(path)
    assert True == config('KeyFallback', cast=bool)
    del os.environ['KeyFallback']

