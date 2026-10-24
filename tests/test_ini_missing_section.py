# coding: utf-8
from io import StringIO

import pytest
from mock import patch

from decouple import RepositoryIni

try:
    from configparser import InterpolationMissingOptionError
except ImportError:
    from ConfigParser import InterpolationMissingOptionError


@pytest.mark.parametrize('contents', ['', '[other]\nkey=value\n'])
def test_ini_without_settings_raises_keyerror(contents):
    with patch('decouple.open', return_value=StringIO(contents), create=True):
        repository = RepositoryIni('settings.ini')
    assert 'missing' not in repository
    with pytest.raises(KeyError) as error:
        repository['missing']
    assert error.value.args == ('missing',)


@pytest.mark.parametrize('contents', ['', '[other]\nkey=value\n'])
def test_ini_without_settings_allows_repository_fallback(contents):
    with patch('decouple.open', return_value=StringIO(contents), create=True):
        repository = RepositoryIni('settings.ini')

    def lookup(key):
        for source in (repository, {'fallback': 'value'}):
            try:
                return source[key]
            except KeyError:
                pass
        raise KeyError(key)

    assert lookup('fallback') == 'value'


def test_ini_preserves_interpolation_errors():
    contents = '[settings]\nkey=%(missing)s\n'
    with patch('decouple.open', return_value=StringIO(contents), create=True):
        repository = RepositoryIni('settings.ini')
    assert 'key' in repository
    with pytest.raises(InterpolationMissingOptionError):
        repository['key']
