# coding: utf-8
import os
import pytest

from decouple import Config, RepositoryConsul, UndefinedValueError

class FakeConsul(object):
    """This class is a monkey patch to simulate consul.Consul.kv.get"""
    def __init__(self, fake_data=None):
        self.fake_data = fake_data or {}
        class KV:
            idx = 0
            @classmethod
            def get(cls, key):
                cls.idx += 1
                if key in self.fake_data:
                    return cls.idx, {'Value': self.fake_data[key]}
                return cls.idx, None
        self.kv = KV()


@pytest.fixture
def consul():
    c = FakeConsul()
    c.fake_data['myapp/secret_key'] = 'some really secure secret key'
    c.fake_data['myapp/debug'] = False
    c.fake_data['staging/debug'] = True
    c.fake_data['unaccessible'] = 'not be accessible if root is set to `myapp`'
    return c


@pytest.fixture
def config(consul):
    return Config(RepositoryConsul(consul, 'myapp'))


def test_consul_undefined(config):
    with pytest.raises(UndefinedValueError):
        # `unaccessible` is defined in a scope that this consul repository
        # has no access to
        config('unaccessible')


def test_consul_get_bool(config):
    assert config('debug', cast=bool) is False


def test_consul_basic(config):
    os.environ['unaccessible'] = 'overwrite'
    assert config('unaccessible') == 'overwrite'
    del os.environ['unaccessible']