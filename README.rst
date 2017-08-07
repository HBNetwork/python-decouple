Python Decouple: Strict separation of settings from code
========================================================

*Decouple* helps you to organize your settings so that you can
change parameters without having to redeploy your app.

It also makes easy for you to:

#. store parameters on *ini* or *.env* files;
#. define comprehensive default values;
#. properly convert values to the correct data type;
#. have **only one** configuration module to rule all your instances.

It was originally designed for Django, but became an independent generic tool
for separating settings from code.

.. image:: https://img.shields.io/travis/henriquebastos/python-decouple.svg
    :target: https://travis-ci.org/henriquebastos/python-decouple
    :alt: Build Status

.. image:: https://landscape.io/github/henriquebastos/python-decouple/master/landscape.png
    :target: https://landscape.io/github/henriquebastos/python-decouple/master
    :alt: Code Health

.. image:: https://img.shields.io/pypi/v/python-decouple.svg
    :target: https://pypi.python.org/pypi/python-decouple/
    :alt: Latest PyPI version



.. contents:: Summary


Why?
====

Web framework's settings stores many different kinds of parameters:

* Locale and i18n;
* Middlewares and Installed Apps;
* Resource handles to the database, Memcached, and other backing services;
* Credentials to external services such as Amazon S3 or Twitter;
* Per-deploy values such as the canonical hostname for the instance.

The first 2 are *project settings* the last 3 are *instance settings*.

You should be able to change *instance settings* without redeploying your app.

Why not just use environment variables?
---------------------------------------

*Envvars* works, but since ``os.environ`` only returns strings, it's tricky.

Let's say you have an *envvar* ``DEBUG=False``. If you run:

.. code-block:: python

    if os.environ['DEBUG']:
        print True
    else:
        print False

It will print **True**, because ``os.environ['DEBUG']`` returns the **string** ``"False"``.
Since it's a non-empty string, it will be evaluated as True.

*Decouple* provides a solution that doesn't look like a workaround: ``config('DEBUG', cast=bool)``.

Usage
=====

Install:

.. code-block:: console

    pip install python-decouple


Then use it on your ``settings.py``.

#. Import the ``config`` object:

   .. code-block:: python

     from decouple import config

#. Retrieve the configuration parameters:

   .. code-block:: python

     SECRET_KEY = config('SECRET_KEY')
     DEBUG = config('DEBUG', default=False, cast=bool)
     EMAIL_HOST = config('EMAIL_HOST', default='localhost')
     EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)

Where the settings data are stored?
-----------------------------------

*Decouple* supports both *.ini* and *.env* files.

Ini file
~~~~~~~~

Simply create a ``settings.ini`` next to your configuration module in the form:

.. code-block:: ini

    [settings]
    DEBUG=True
    TEMPLATE_DEBUG=%(DEBUG)s
    SECRET_KEY=ARANDOMSECRETKEY
    DATABASE_URL=mysql://myuser:mypassword@myhost/mydatabase
    PERCENTILE=90%%
    #COMMENTED=42

*Note*: Since ``ConfigParser`` supports *string interpolation*, to represent the character ``%`` you need to escape it as ``%%``.

Env file
~~~~~~~~

Simply create a ``.env`` text file on your repository's root directory in the form:

.. code-block:: console

    DEBUG=True
    TEMPLATE_DEBUG=True
    SECRET_KEY=ARANDOMSECRETKEY
    DATABASE_URL=mysql://myuser:mypassword@myhost/mydatabase
    PERCENTILE=90%
    #COMMENTED=42

Example: How do I use it with Django?
-------------------------------------

Given that I have a ``.env`` file at my repository root directory, here is a snippet of my ``settings.py``.

I also recommend using `pathlib <https://docs.python.org/3/library/pathlib.html>`_
and `dj-database-url <https://pypi.python.org/pypi/dj-database-url/>`_.

.. code-block:: python

    # coding: utf-8
    from decouple import config
    from unipath import Path
    from dj_database_url import parse as db_url


    BASE_DIR = Path(__file__).parent

    DEBUG = config('DEBUG', default=False, cast=bool)
    TEMPLATE_DEBUG = DEBUG

    DATABASES = {
        'default': config(
            'DATABASE_URL',
            default='sqlite:///' + BASE_DIR.child('db.sqlite3'),
            cast=db_url
        )
    }

    TIME_ZONE = 'America/Sao_Paulo'
    USE_L10N = True
    USE_TZ = True

    SECRET_KEY = config('SECRET_KEY')

    EMAIL_HOST = config('EMAIL_HOST', default='localhost')
    EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
    EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
    EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)

    # ...

Attention with *undefined* parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On the above example, all configuration parameters except ``SECRET_KEY = config('SECRET_KEY')``
have a default value to fallback if it does not exist on the ``.env`` file.

If ``SECRET_KEY`` is not present on the ``.env``, *decouple* will raise an ``UndefinedValueError``.

This *fail fast* policy helps you avoid chasing misbehaviors when you eventually forget a parameter.

Overriding config files with environment variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some times you may want to change a parameter value without having to edit the ``.ini`` or ``.env`` files.

Since version 3.0, *decouple* respect the *unix way*.
Therefore environment variables have precedence over config files.

To override a config parameter you can simply do:

.. code-block:: console

    DEBUG=True python manage.py


How it works?
=============

*Decouple* always searches for *Options* in this order:

#. Environment variables;
#. Repository: ini or .env file;
#. default argument passed to config.

There are 4 classes doing the magic:


- ``Config``

    Coordinates all the configuration retrieval.

- ``RepositoryIni``

    Can read values from ``os.environ`` and ini files, in that order.

    **Note:** Since version 3.0 *decouple* respects unix precedence of environment variables *over* config files.

- ``RepositoryEnv``

    Can read values from ``os.environ`` and ``.env`` files.

    **Note:** Since version 3.0 *decouple* respects unix precedence of environment variables *over* config files.

- ``AutoConfig``

    This is a *lazy* ``Config`` factory that detects which configuration repository you're using.

    It recursively searches up your configuration module path looking for a
    ``settings.ini`` or a ``.env`` file.

    Optionally, it accepts ``search_path`` argument to explicitly define
    where the search starts.

The **config** object is an instance of ``AutoConfig`` that instantiates a ``Config`` with the proper ``Repository``
on the first time it is used.


Understanding the CAST argument
-------------------------------

By default, all values returned by `decouple` are `strings`, after all they are
read from `text files` or the `envvars`.

However, your Python code may expect some other value type, for example:

* Django's DEBUG expects a boolean True or False.
* Django's EMAIL_PORT expects an integer.
* Django's ALLOWED_HOSTS expects a list of hostnames.
* Django's SECURE_PROXY_SSL_HEADER expects a tuple with two elements, the name of the header to look for and the required value.

To meet this need, the `config` function accepts a `cast` argument which
receives any *callable*, that will be used to *transform* the string value
into something else.

Let's see some examples for the above mentioned cases:

.. code-block:: pycon

    >>> os.environ['DEBUG'] = 'False'
    >>> config('DEBUG', cast=bool)
    False

    >>> os.environ['EMAIL_PORT'] = '42'
    >>> config('EMAIL_PORT', cast=int)
    42

    >>> os.environ['ALLOWED_HOSTS'] = '.localhost, .herokuapp.com'
    >>> config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])
    ['.localhost', '.herokuapp.com']

    >>> os.environ['SECURE_PROXY_SSL_HEADER'] = 'HTTP_X_FORWARDED_PROTO, https'
    >>> config('SECURE_PROXY_SSL_HEADER', cast=Csv(tuple_=True))
    ('HTTP_X_FORWARDED_PROTO', 'https')

As you can see, `cast` is very flexible. But the last example got a bit complex.

Built in Csv Helper
~~~~~~~~~~~~~~~~~~~

To address the complexity of the last example, *Decouple* comes with an extensible *Csv helper*.

Let's improve the last example:

.. code-block:: pycon

    >>> from decouple import Csv
    >>> os.environ['ALLOWED_HOSTS'] = '.localhost, .herokuapp.com'
    >>> config('ALLOWED_HOSTS', cast=Csv())
    ['.localhost', '.herokuapp.com']

You can also parametrize the *Csv Helper* to return other types of data.

.. code-block:: pycon

    >>> os.environ['LIST_OF_INTEGERS'] = '1,2,3,4,5'
    >>> config('LIST_OF_INTEGERS', cast=Csv(int))
    [1, 2, 3, 4, 5]

    >>> os.environ['COMPLEX_STRING'] = '%virtual_env%\t *important stuff*\t   trailing spaces   '
    >>> csv = Csv(cast=lambda s: s.upper(), delimiter='\t', strip=' %*')
    >>> csv(os.environ['COMPLEX_STRING'])
    ['VIRTUAL_ENV', 'IMPORTANT STUFF', 'TRAILING SPACES']

Contribute
==========

Your contribution is welcome.

Setup you development environment:

.. code-block:: console

    git clone git@github.com:henriquebastos/python-decouple.git
    cd python-decouple
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    tox

*Decouple* supports both Python 2.7 and 3.6. Make sure you have both installed.

I use `pyenv <https://github.com/pyenv/pyenv#simple-python-version-management-pyenv>`_ to
manage multiple Python versions and I described my workspace setup on this article:
`The definitive guide to setup my Python workspace
<https://medium.com/@henriquebastos/the-definitive-guide-to-setup-my-python-workspace-628d68552e14>`_

You can submit pull requests and issues for discussion. However I only
consider merge tested code.


License
=======

The MIT License (MIT)

Copyright (c) 2017 Henrique Bastos <henrique at bastos dot net>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
