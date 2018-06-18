# coding: utf-8
import os

from decouple import Config, RepositorySecret


def test_secrets():
    path = os.path.join(os.path.dirname(__file__), 'secrets')
    config = Config(RepositorySecret(path))

    assert 'hello' == config('db_user')
    assert 'world' == config('db_password')


def test_env_undefined_but_present_in_os_environ():
    path = os.path.join(os.path.dirname(__file__), 'secrets')
    config = Config(RepositorySecret(path))

    os.environ['KeyOnlyEnviron'] = ''
    assert '' == config('KeyOnlyEnviron')
    del os.environ['KeyOnlyEnviron']
