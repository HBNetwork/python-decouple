# coding: utf-8
from decouple import MultiConfig, RepositoryDict, RepositoryIni, DoesNotExist, UnsupportedExtensionError
import os
import pytest

repository_dict = RepositoryDict(dict(
    DICT_SETTING='dict',
    SHARED_SETTING='dict',
))


def test_multiconfig_settings_from_each_file():
    config = MultiConfig('.os', repository_dict, 'tests/multiconfig/config.env', 'tests/multiconfig/config.ini', 'tests/multiconfig/config.py', 'tests/multiconfig/config.json')
    config.supported_extensions['ini'] = RepositoryIni
    os.environ['OS_SETTING'] = 'os'
    assert 'os' == config('OS_SETTING')
    assert 'dict' == config('DICT_SETTING')
    assert 'env' == config('ENV_SETTING')
    assert 'ini' == config('ini_setting')  # Note that the key has been transformed to lower case by the .ini ConfigParser
    assert 'py' == config('PY_SETTING')
    assert 'json' == config('JSON_SETTING')


def test_multiconfig_priority_os():
    config = MultiConfig('.os', repository_dict, 'tests/multiconfig/config.env', 'tests/multiconfig/config.ini', 'tests/multiconfig/config.py', 'tests/multiconfig/config.json')
    config.supported_extensions['ini'] = RepositoryIni
    os.environ['SHARED_SETTING'] = 'os'
    assert 'os' == config('SHARED_SETTING')


def test_multiconfig_priority_dict():
    config = MultiConfig(repository_dict, '.os', 'tests/multiconfig/config.env', 'tests/multiconfig/config.ini', 'tests/multiconfig/config.py', 'tests/multiconfig/config.json')
    config.supported_extensions['ini'] = RepositoryIni
    os.environ['SHARED_SETTING'] = 'os'
    assert 'dict' == config('SHARED_SETTING')


def test_multiconfig_priority_env():
    config = MultiConfig('tests/multiconfig/config.env', '.os', repository_dict, 'tests/multiconfig/config.ini', 'tests/multiconfig/config.py', 'tests/multiconfig/config.json')
    config.supported_extensions['ini'] = RepositoryIni
    os.environ['SHARED_SETTING'] = 'os'
    assert 'env' == config('SHARED_SETTING')


def test_multiconfig_priority_ini():
    config = MultiConfig('tests/multiconfig/config.ini', '.os', repository_dict, 'tests/multiconfig/config.env', 'tests/multiconfig/config.py', 'tests/multiconfig/config.json')
    config.supported_extensions['ini'] = RepositoryIni
    os.environ['SHARED_SETTING'] = 'os'
    assert 'ini' == config('ini_setting')  # Note that the key has been transformed to lower case by the .ini ConfigParser


def test_multiconfig_priority_py():
    config = MultiConfig('tests/multiconfig/config.py', '.os', repository_dict, 'tests/multiconfig/config.env', 'tests/multiconfig/config.ini', 'tests/multiconfig/config.json')
    config.supported_extensions['ini'] = RepositoryIni
    os.environ['SHARED_SETTING'] = 'os'
    assert 'py' == config('SHARED_SETTING')


def test_multiconfig_priority_json():
    config = MultiConfig('tests/multiconfig/config.json', '.os', repository_dict, 'tests/multiconfig/config.env', 'tests/multiconfig/config.ini', 'tests/multiconfig/config.py')
    config.supported_extensions['ini'] = RepositoryIni
    os.environ['SHARED_SETTING'] = 'os'
    assert 'json' == config('SHARED_SETTING')


def test_multiconfig_not_found_env():
    config = MultiConfig('.os')
    with pytest.raises(DoesNotExist):
        config('ANY_KEY')


def test_multiconfig_not_found_env():
    config = MultiConfig('nofile.json')
    with pytest.raises(DoesNotExist):
        config('ANY_KEY')


def test_multiconfig_not_found_ini():
    config = MultiConfig('nofile.ini')
    config.supported_extensions['ini'] = RepositoryIni
    with pytest.raises(DoesNotExist):
        config('ANY_KEY')


def test_multiconfig_not_found_py():
    config = MultiConfig('nofile.py')
    with pytest.raises(DoesNotExist):
        config('ANY_KEY')


def test_multiconfig_not_found_json():
    config = MultiConfig('nofile.json')
    with pytest.raises(DoesNotExist):
        config('ANY_KEY')


def test_ini_not_supported_by_default():
    config = MultiConfig('nofile.ini')
    with pytest.raises(UnsupportedExtensionError):
        config('ANY_KEY')

