Changelog
=========

3.7 (2023-01-09)
----------------

- Fix `Csv` cast hanging with `default=None`, now returning an empty list. (#149)

3.6 (2022-02-02)
----------------

- Add support for Docker secrets.
- Fix deprecation warning on Python 3.10

3.5 (2021-09-30)
----------------

- Fix: fix syntax warnings due to comparison of literals using `is`
- Fix: avoid DeprecationError on ConfigParser.readfp()
- Add Tox Github Action
- Documentation fixups
- Security: bump Pygments version to >=2.7.4
- Fix .env -file quote stripping
- Changelog catchups for 3.2 and 3.3


3.4 (2021-01-05)
----------------

- Add choices helper
- Documentation fixups


3.3 (2019-11-13)
----------------

- Enforce search order in settings files
- Switch to using strtobool (#71)


3.2 (2019-11-13)
----------------

- Fixed typos in documentation
- Add editorconfig file
- Fix handling for configuration values that end in single or double quotes (#78)
- Add support for encoding env files in other encodings (#62) (#64)
- Improve csv documentation (#59)
- Add Changelog #44
- Fixed typo. [Vik]
- Fix the code blocks inline in the documentation, adding two quotes. [Manaia Junior]
- Fixed argument in Csv documentation. [Manaia Junior]


3.1 (2017-08-07)
----------------
- Improve README
- Improve tests
- Add support for Csv to be able to return tuple format. Closes #38. [Henrique Bastos]
- Move Csv doc to proper section. [Henrique Bastos]
- Add a post_process argument do Csv. [Henrique Bastos]
- Add support for Csv to be able to return in tuple format. [Manaia Junior]
- Closes #24. [Henrique Bastos]
- Added empty string as False value. [Rafael Sierra]
- Use context manager when opening files. [Jon Banafato]
- Explicitly name summary section. [Henrique Bastos]
- Simplify Repository hierarchy. [Henrique Bastos]
- Fix code quality. [Henrique Bastos]
- Fix case where Option exists on ENV, but not on repository. [Henrique Bastos] #27
- Allow to override initial search path in AutoConfig class. [Rolando Espinoza]
- Update dependencies. [Henrique Bastos]
- Fixes bug while looking for config file in parent dirs. [Flavio Amieiro]
- Add section explaining environment variable override. [Henrique Bastos]


3.0 (2015-09-15)
----------------
- Update README for 3.0. [Henrique Bastos]
- Force os.environ to override Ini and Env. [Henrique Bastos]


2.4 (2015-09-15)
----------------
- Update requirements. [Henrique Bastos]
- Check if filepath is really a file, not a directory. [Thiago Garcia]
- Fix LIST_OF_INTEGERS CSV example on README. [KS Chan]
- Fix headline marks. [Henrique Bastos]
- Explicitly mention how to comment a line. [Henrique Bastos]
- Typo: A(tt)ention. [Thomas Güttler]


2.3 (2015-03-19)
----------------
- Readme fix adding syntax highlight for python console. [Henrique Bastos]
- Add Csv Helper. [Henrique Bastos]
- Update development dependencies’ versions. [Henrique Bastos]
- Update tox to use python 3.4. [Henrique Bastos]
- Fix annoying error when env lines have non relevant whitespace. [Henrique Bastos]
- Test empty key on ini. [Henrique Bastos]
- Fix #3: return empty string when envvar is empty. [Osvaldo Santana Neto]


2.2 (2015-03-19)
----------------
- Improve README
- Add notice on fail fast policy. [Henrique Bastos]
- Fix boolean conversion of default value. [Henrique Bastos]
- Update setup.py. [Henrique Bastos]
- Add docutils and pygments to development's requirements.txt. [Henrique Bastos]
- Upgrade development dependencies. [Henrique Bastos]
- Fix more landscape reports. [Henrique Bastos]
- Fixing landscape reported issues. [Henrique Bastos]
- Refactor tests to use fixtures. [Henrique Bastos]
- Fix tests to use Repositories. [Henrique Bastos]
- Adapt AutoConfig to use Repositories with Config. [Henrique Bastos]
- Fix RepositoryEnv logic. [Henrique Bastos]
- Unify Config classes into one. [Henrique Bastos]
- Add comments. [Henrique Bastos]
- Remove unused variables. [Henrique Bastos]
- Add Repository classes. [Henrique Bastos]
- Change ConfigEnv behavior to raise when option or default are undefined. [Henrique Bastos]


2.1 (2015-03-19)
----------------
- Test we have access to envvar when we have no file. [Henrique Bastos]
- Deal with access errors. [Henrique Bastos]
- Fix stupid bug on Heroku. [Henrique Bastos]
- Fix inline style on README. [Henrique Bastos]
- Improve explanation about how decouple works. [Henrique Bastos]
- Add build status image. [Henrique Bastos]
- Configure travis-ci. [Henrique Bastos]
- Add tox. [Henrique Bastos]
- Add support for Python3. [Henrique Bastos]
- Implement fallback to os.environ. [Henrique Bastos]
- Remove load method. [Henrique Bastos]
- Isolate logic for reading .env. [Henrique Bastos]


2.0 (2015-03-19)
----------------
- Improve README. [Henrique Bastos]
- Move exception to a better context. [Henrique Bastos]
- Replace cwd with current module's path. [Henrique Bastos]
- Add a requirements.txt for developers. [Henrique Bastos]
- Implement AutoConfig. [Henrique Bastos]
- Extract the basic API to a base class. [Henrique Bastos]
- Implement ConfigEnv. [Henrique Bastos]
- Add tests to ConfigIni. [Henrique Bastos]
- Make sure to initialize instance attributes. [Henrique Bastos]
- Ignore PyCharm project dir. [Henrique Bastos]


1.0 (2015-03-19)
----------------
- Improve API replacing type with cast. [Henrique Bastos]
- Import code. [Henrique Bastos]
- Add license, readme and setup. [Henrique Bastos]
