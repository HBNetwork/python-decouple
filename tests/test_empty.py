import pytest

from decouple import Config, RepositoryEmpty, UndefinedValueError


@pytest.mark.parametrize('key', ['MISSING', '', None, 42])
def test_empty_repository_missing_key(key):
    repository = RepositoryEmpty()

    assert key not in repository
    with pytest.raises(KeyError) as error:
        repository[key]
    assert error.value.args == (key,)


def test_empty_repository_config_missing(monkeypatch):
    monkeypatch.delenv('DECOUPLE_EMPTY_TEST', raising=False)
    config = Config(RepositoryEmpty())

    with pytest.raises(UndefinedValueError):
        config('DECOUPLE_EMPTY_TEST')
    assert config('DECOUPLE_EMPTY_TEST', default=None) is None
    assert config('DECOUPLE_EMPTY_TEST', default='42', cast=int) == 42


@pytest.mark.parametrize('value', ['', 'from environment'])
def test_empty_repository_config_environment(monkeypatch, value):
    monkeypatch.setenv('DECOUPLE_EMPTY_TEST', value)
    repository = RepositoryEmpty()

    assert 'DECOUPLE_EMPTY_TEST' not in repository
    with pytest.raises(KeyError):
        repository['DECOUPLE_EMPTY_TEST']
    assert Config(repository)('DECOUPLE_EMPTY_TEST', default='fallback') == value
