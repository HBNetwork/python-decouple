# coding: utf-8
import os

import pytest

from decouple import Config, RepositoryIni, UndefinedValueError, RepositoryEnv

FILE = '''
[settings]
KeyTrue=True
KeyOne=1
KeyYes=yes
KeyOn=on

KeyFalse=False
KeyZero=0
KeyNo=no
KeyOff=off
KeyEmpty=

#CommentedKey=None
PercentIsEscaped=%%
PercentNotEscaped=%%
Interpolation=%(KeyOff)s
NoInterpolation=%(KeyOff)s
IgnoreSpace = text
KeyOverrideByEnv=NotThis
KeyUTF8=значение
'''


@pytest.fixture(scope='module')
def configs():
    encoding = 'utf8'
    env_path, ini_path = write_files(encoding)
    yield [Config(RepositoryEnv(env_path, encoding)), Config(RepositoryIni(ini_path, encoding))]
    clean((env_path, ini_path))


def clean(files):
    for file in files:
        os.unlink(file)


def write_files(encoding):
    env_path = '.env'
    ini_path = 'settings.ini'
    write_file(env_path, encoding)
    write_file(ini_path, encoding)
    return env_path, ini_path


def write_file(path, encoding='utf8'):
    with open(path, 'w', encoding=encoding) as f:
        f.write(FILE)


def test_comment(configs):
    assert_all_raises(configs, 'CommentedKey', UndefinedValueError)


def test_ini_percent_escape(configs):
    assert '%' == configs[1]('PercentIsEscaped')


def test_env_percent_not_escaped(configs):
    assert '%%' == configs[0]('PercentNotEscaped')


def test_ini_interpolation(configs):
    assert 'off' == configs[1]('Interpolation')


def test_env_no_interpolation(configs):
    assert '%(KeyOff)s' == configs[0]('NoInterpolation')


def test_bool_true(configs):
    keys = ['KeyTrue', 'KeyOne', 'KeyYes', 'KeyOn']
    assert_keys_with_same_value_are_equals(configs, keys, True, {'cast': bool})


def test_bool_false(configs):
    keys = ['KeyFalse', 'KeyZero', 'KeyNo', 'KeyOff']
    assert_keys_with_same_value_are_equals(configs, keys, False, {'cast': bool})


def assert_keys_with_same_value_are_equals(configs, keys, expected, config_kwargs=None):
    for key in keys:
        assert_all_equals(configs, key, expected, config_kwargs)


def test_undefined(configs):
    assert_all_raises(configs, 'UndefinedKey', UndefinedValueError)


def test_default_none(configs):
    assert_all_are_none(configs, 'UndefinedKey', {'default': None})


def test_default_bool(configs):
    assert_all_equals(configs, 'UndefinedKey', False, {'default': False, 'cast': bool})
    assert_all_equals(configs, 'UndefinedKey', True, {'default': True, 'cast': bool})


def test_default(configs):
    assert_all_equals(configs, 'UndefinedKey', True, {'default': True})
    assert_all_equals(configs, 'UndefinedKey', False, {'default': False})


def test_default_invalid_bool(configs):
    assert_all_raises(configs, 'UndefinedKey', ValueError, {'default': 'NotBool', 'cast': bool})


def test_empty(configs):
    assert_all_equals(configs, 'KeyEmpty', '', {'default': None})


def test_support_space(configs):
    assert_all_equals(configs, 'IgnoreSpace', 'text')


def test_os_environ(configs):
    key = 'KeyOverrideByEnv'
    value = 'This'
    os.environ[key] = value
    assert_all_equals(configs, key, value)
    del os.environ[key]


def test_undefined_but_present_in_os_environ(configs):
    key = 'KeyOnlyEnviron'
    value = ''
    os.environ[key] = value
    assert_all_equals(configs, key, value)
    del os.environ[key]


def test_empty_string_means_false(configs):
    assert_all_equals(configs, 'KeyEmpty', False, {'cast': bool})


def test_utf8_value(configs):
    assert_all_equals(configs, 'KeyUTF8', 'значение')


def test_another_encoding():
    encoding = 'cp1251'
    env_path, ini_path = write_files(encoding)
    configs = [Config(RepositoryEnv(env_path, encoding)), Config(RepositoryIni(ini_path, encoding))]
    assert_all_equals(configs, 'KeyUTF8', 'значение')


def assert_all_equals(configs, key, expected, config_kwargs=None):
    config_kwargs = set_dict_is_none(config_kwargs)
    for config in configs:
        assert expected == config(key, **config_kwargs)


def assert_all_raises(configs, key, exception=Exception, config_kwargs=None):
    config_kwargs = set_dict_is_none(config_kwargs)
    for config in configs:
        with pytest.raises(exception):
            config(key, **config_kwargs)


def assert_all_are_none(configs, key, config_kwargs=None):
    config_kwargs = set_dict_is_none(config_kwargs)
    for config in configs:
        assert config(key, **config_kwargs) is None


def set_dict_is_none(dict_):
    return {} if dict_ is None else dict_
