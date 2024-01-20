# coding: utf-8
import os
import pytest
from decouple import Config, RepositoryGoogleSecretManager, UndefinedValueError

ENVSTRING = """
KeyTrue=True\nKeyOne=1\nKeyYes=yes
KeyY=y
KeyOn=on

KeyFalse=False
KeyZero=0
KeyNo=no
KeyN=n
KeyOff=off
KeyEmpty=

# CommentedKey=None
KeyWithSpaces = Some Value With Spaces
KeyWithQuotes="Quoted Value"
"""


@pytest.fixture(scope="module")
def config():
    return Config(RepositoryGoogleSecretManager(ENVSTRING))


def test_string_comment(config):
    with pytest.raises(UndefinedValueError):
        config("CommentedKey")


def test_string_bool_true(config):
    assert config("KeyTrue", cast=bool)
    assert config("KeyOne", cast=bool)
    assert config("KeyYes", cast=bool)
    assert config("KeyY", cast=bool)
    assert config("KeyOn", cast=bool)


def test_string_bool_false(config):
    assert not config("KeyFalse", cast=bool)
    assert not config("KeyZero", cast=bool)
    assert not config("KeyNo", cast=bool)
    assert not config("KeyOff", cast=bool)
    assert not config("KeyN", cast=bool)
    assert not config("KeyEmpty", cast=bool)


def test_string_undefined(config):
    with pytest.raises(UndefinedValueError):
        config("UndefinedKey")


def test_string_default_none(config):
    assert config("UndefinedKey", default=None) is None


def test_string_default_bool(config):
    assert not config("UndefinedKey", default=False, cast=bool)
    assert config("UndefinedKey", default=True, cast=bool)


def test_string_default(config):
    assert not config("UndefinedKey", default=False)
    assert config("UndefinedKey", default=True)


def test_string_default_invalid_bool(config):
    with pytest.raises(ValueError):
        config("UndefinedKey", default="NotBool", cast=bool)


def test_string_empty(config):
    assert config("KeyEmpty", default=None) == ""


def test_string_support_space(config):
    assert config("KeyWithSpaces") == "Some Value With Spaces"


def test_string_os_environ(config):
    os.environ["KeyOverrideByEnv"] = "This"
    assert config("KeyOverrideByEnv") == "This"
    del os.environ["KeyOverrideByEnv"]


def test_string_undefined_but_present_in_os_environ(config):
    os.environ["KeyOnlyEnviron"] = ""
    assert config("KeyOnlyEnviron") == ""
    del os.environ["KeyOnlyEnviron"]


def test_string_empty_string_means_false(config):
    assert not config("KeyEmpty", cast=bool)


def test_string_repo_keyerror(config):
    with pytest.raises(KeyError):
        config.repository["UndefinedKey"]


def test_string_quoted_value(config):
    assert config("KeyWithQuotes") == "Quoted Value"
