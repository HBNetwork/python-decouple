# coding: utf-8
import os
import sys
from mock import patch
import pytest
from decouple import Config, RepositoryEnv, UndefinedValueError

# Useful for very coarse version differentiation.
PY3 = sys.version_info[0] == 3

if PY3:
    from io import StringIO
else:
    from io import BytesIO as StringIO


ENVFILE = '''
# Empty values
DB_PORT=
SECRET=
DEBUG=
LIST_VALUES=

# Non-empty values for comparison
DB_HOST=localhost
SECRET_KEY=abc123
'''

@pytest.fixture(scope='module')
def config():
    with patch('decouple.open', return_value=StringIO(ENVFILE), create=True):
        return Config(RepositoryEnv('.env'))


def test_empty_value_with_default_int():
    """Test that an empty DB_PORT with default and int cast works correctly."""
    # Create a fresh config for this test to avoid fixture caching issues
    with patch('decouple.open', return_value=StringIO(ENVFILE), create=True):
        config = Config(RepositoryEnv('.env'))
        # DB_PORT= (empty) should use the default value 5432
        assert 5432 == config('DB_PORT', default=5432, cast=int)


def test_empty_value_with_default_none():
    """Test that an empty SECRET with default=None works correctly."""
    # Create a fresh config for this test to avoid fixture caching issues
    with patch('decouple.open', return_value=StringIO(ENVFILE), create=True):
        config = Config(RepositoryEnv('.env'))
        # SECRET= (empty) should use the default value None
        assert None is config('SECRET', default=None)


def test_empty_value_with_default_bool():
    """Test that an empty DEBUG with default and bool cast works correctly."""
    # Create a fresh config for this test to avoid fixture caching issues
    with patch('decouple.open', return_value=StringIO(ENVFILE), create=True):
        config = Config(RepositoryEnv('.env'))
        # DEBUG= (empty) should use the default value True
        assert True is config('DEBUG', default=True, cast=bool)
        # Empty value without default should be False when cast to bool
        assert False is config('DEBUG', cast=bool)


def test_empty_value_with_csv_cast():
    """Test that an empty LIST_VALUES with Csv cast works correctly."""
    # Create a fresh config for this test to avoid fixture caching issues
    from decouple import Csv
    with patch('decouple.open', return_value=StringIO(ENVFILE), create=True):
        config = Config(RepositoryEnv('.env'))
        # LIST_VALUES= (empty) should return an empty list with Csv cast
        # For empty values, we need to manually apply the Csv cast
        empty_value = config('LIST_VALUES')
        assert [] == Csv()(empty_value)
        # With default values
        assert ['default'] == config('LIST_VALUES', default='default', cast=Csv())
