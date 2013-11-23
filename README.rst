Django Decouple: Strict separation of settings from code
========================================================

*Decouple* helps you to organize your settings so that you can
change parameters without having to redeploy your app.

Why?
----

Django's settings stores many different kind of parameters:

* Locale and i18n

* Middlewares and Installed Apps

* Resource handles to the database, Memcached, and other backing services

* Credentials to external services such as Amazon S3 or Twitter

* Per-deploy values such as the canonical hostname for the deploy

The first 2 items are *project settings* the last 3 are *instance settings*.

You should be able to change *instance settings* without redeploying your app.

Install
-------

.. code-block:: console

    pip install django-decouple

Usage
-----

Use it on your ``settings.py``.

#. Import the ``Config`` class:

.. code-block:: python

    from decouple import Config

#. Instantiate it passing the config storage:

.. code-block:: python

    config = Config('settings.ini')

#. Retrieve the configuration parameters:

.. code-block:: python

    SECRET_KEY = config('SECRET_KEY')
    DEBUG = config('DEBUG', default=False, cast=bool)
    EMAIL_HOST = config('EMAIL_HOST', default='localhost')
    EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)


How I use it
------------

Bellow there is a snippet of a ``settings.py``.

I also recommend using `unipath <https://pypi.python.org/pypi/Unipath>`_
and `dj-datatabase-url <https://pypi.python.org/pypi/dj-database-url/>`_.

.. code-block:: python

    # coding: utf-8
    from unipath import Path
    from decouple import Config
    from dj_database_url import db_url


    PROJECT_ROOT = Path(__file__).parent

    config = Config(PROJECT_ROOT.child('settings.ini'))

    DEBUG = config('DEBUG', default=False, cast=bool)
    TEMPLATE_DEBUG = DEBUG

    DATABASES = {
        'default': config(
            'DATABASE_URL',
            default='sqlite:///' + PROJECT_ROOT.child('database.db'),
            cast=db_url
        )
    }

    SITE_ID = 1

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

A sample INI file
-----------------

    [settings]
    DEBUG=True
    SECRET_KEY=ARANDOMSECRETKEY
    DATABASE_URL=mysql://myuser:mypassword@myhost/mydatabase
    PERCENTILE=90%%

Note: Since you can use *string interpolation* on values, to represent the character `%` you need to escape it as `%%`.

License
=======

The MIT License.
