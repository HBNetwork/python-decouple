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
    config = AutoConfig()
    with patch('os.path.exists', return_value=False):
        with patch.object(config, '_caller_path', return_value="/"):
            with pytest.raises(RuntimeError):
                config('KEY')
