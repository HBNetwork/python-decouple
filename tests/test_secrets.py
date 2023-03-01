# coding: utf-8
import os
import pytest

from decouple import Config, RepositorySecret


def test_secrets():
    path = os.path.join(os.path.dirname(__file__), 'secrets')
    config = Config(RepositorySecret(path))

    assert 'hello' == config('db_user')
    assert 'world' == config('db_password')


def test_no_secret_but_present_in_os_environ():
    path = os.path.join(os.path.dirname(__file__), 'secrets')
    config = Config(RepositorySecret(path))

    os.environ['KeyOnlyEnviron'] = 'SOMETHING'
    assert 'SOMETHING' == config('KeyOnlyEnviron')
    del os.environ['KeyOnlyEnviron']


def test_secret_overriden_by_environ():
    path = os.path.join(os.path.dirname(__file__), 'secrets')
    config = Config(RepositorySecret(path))

    os.environ['db_user'] = 'hi'
    assert 'hi' == config('db_user')
    del os.environ['db_user']

def test_secret_repo_keyerror():
    path = os.path.join(os.path.dirname(__file__), 'secrets')
    repo = RepositorySecret(path)

    with pytest.raises(KeyError):
        repo['UndefinedKey']
