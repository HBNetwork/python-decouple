Django Decouple: Strict separation of settings from code
========================================================

*Decouple* helps you to organize your settings so that you can
change parameters without having to redeploy your app.

It also makes easy for you to:

#. store parameters on *ini* or *.env* files;
#. define comprehensive default values;
#. properly convert values to the correct data type;
#. have **only one** ``settings.py`` to rule all your instances.

.. image:: https://travis-ci.org/henriquebastos/django-decouple.png?branch=master
    :target: https://travis-ci.org/henriquebastos/django-decouple

Why?
----

Django's settings stores many different kinds of parameters:

* Locale and i18n;
* Middlewares and Installed Apps;
* Resource handles to the database, Memcached, and other backing services;
* Credentials to external services such as Amazon S3 or Twitter;
* Per-deploy values such as the canonical hostname for the instance.

The first 2 are *project settings* the last 3 are *instance settings*.

You should be able to change *instance settings* without redeploying your app.

What about environment variables?
---------------------------------

*Envvars* works, but since ``os.environ`` only returns strings, it's tricky.

Let's say you have an *envvar* ``DEBUG=False``. If you run:

.. code-block:: python

    if os.environ['DEBUG']:
        print True
    else:
        print False

It will print **True**, because ``os.environ['DEBUG']`` returns the **string** ``"False"``.

*Decouple* provides a solution that doesn't look like a workaround: ``config('DEBUG', cast=bool)``.

Install
-------

.. code-block:: console

    pip install django-decouple

Usage
-----

On your ``settings.py``.

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
~~~~~~~~~

Simply create a ``settings.ini`` next to your ``settings.py`` in the form:

.. code-block:: ini

    [settings]
    DEBUG=True
    TEMPLATE_DEBUG=%(DEBUG)s
    SECRET_KEY=ARANDOMSECRETKEY
    DATABASE_URL=mysql://myuser:mypassword@myhost/mydatabase
    PERCENTILE=90%%

*Note*: Since ``ConfigParser`` supports *string interpolation*, to represent the character ``%`` you need to escape it as ``%%``.

Env file
~~~~~~~~~

Simply create a ``.env`` text file on your repository's root directory in the form:

.. code-block:: console

    DEBUG=True
    TEMPLATE_DEBUG=True
    SECRET_KEY=ARANDOMSECRETKEY
    DATABASE_URL=mysql://myuser:mypassword@myhost/mydatabase
    PERCENTILE=90%

How do I use it?
----------------

Given that I have a ``.env`` file at my repository root directory, here is a snippet of my ``settings.py``.

I also recommend using `unipath <https://pypi.python.org/pypi/Unipath>`_
and `dj-datatabase-url <https://pypi.python.org/pypi/dj-database-url/>`_.

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
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
    EMAIL_HOST_USER = config('EMAIL_HOST_USER')
    EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)

    # ...

How it works?
-------------

*Decouple* is made of 3 classes:

- ``ConfigIni``

    Can read and write ini files.

- ``ConfigEnv``

    Can read ``.env`` files and when a parameter does not exist there,
    it tries to find it on ``os.environ``.

    This process does **not** change nor add any environment variables.

- ``AutoConfig``

    Recursively searches up your ``settings.py`` path looking for a
    ``settings.ini`` or a ``.env`` file.

The **config** object is a default instance of ``AutoConfig`` to improve
*decouple*'s usage.

If you prefer or need to explicitly define your storage file, directly use
``ConfigIni`` or ``ConfigEnv``.

License
=======

The MIT License (MIT)

Copyright (c) 2013 Henrique Bastos <henrique at bastos dot net>

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
