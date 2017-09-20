Changelog
=========


(unreleased)
------------
- Fixed typo. [Vik]
- Fix the code blocks inline in the documentation, adding two quotes. [Manaia Junior]
- Fixed argument in Csv documentation. [Manaia Junior]


3.1 (2017-08-07)
----------------
- Bump version. [Henrique Bastos]
- Add support for Csv to be able to return tuple format. Closes #38. [Henrique Bastos]
- Move Csv doc to proper section. [Henrique Bastos]
- Add a post_process argument do Csv. [Henrique Bastos]
- Fix indent. [Henrique Bastos]
- Add to README an example using the tuple format in Csv. [Manaia Junior]
- Add support for Csv to be able to return in tuple format. [Manaia Junior]
- Closes #24. [Henrique Bastos]
- Improving tests. [Henrique Bastos]
- Added empty string as False value. [Rafael Sierra]
- Use context manager when opening files. [Jon Banafato]
- Explicitly name summary section. [Henrique Bastos]
- Add a summary to README. [Henrique Bastos]
- Add contribute section to README. [Henrique Bastos]
- Improve README. [Henrique Bastos] #29
- Simplify Repository hierarchy. [Henrique Bastos]
- Fix code quality. [Henrique Bastos]
- Fix case where Option exists on ENV, but not on repository. [Henrique Bastos] #27
- Improve test_env. [Henrique Bastos]
- Improve README. [Henrique Bastos]
- Make custom path test more explicit. [Henrique Bastos]
- Allow to override initial search path in AutoConfig class. [Rolando Espinoza]
- Update README. [Henrique Bastos]
- Update dependencies. [Henrique Bastos]
- Improve README: fix examples and typos. [Daniel Hahler]
- Fixes bug while looking for config file in parent dirs. [Flavio Amieiro]
- Remove outdated badge. [Henrique Bastos]
- Add section explaining environment variable override. [Henrique Bastos]


3.0 (2015-09-15)
----------------
- Bump version to 3.0. [Henrique Bastos]
- Update README for 3.0. [Henrique Bastos]
- Force os.environ to override Ini and Env. [Henrique Bastos]


2.4 (2015-09-15)
----------------
- Bump version to 2.4. [Henrique Bastos]
- Update requirements. [Henrique Bastos]
- Check if filepath is really a file, not a directory. [Thiago Garcia]
- Fix LIST_OF_INTEGERS CSV example on README. [KS Chan]
- Fix headline marks. [Henrique Bastos]
- Explicitly mention how to comment a line. [Henrique Bastos]
- Typo: A(tt)ention. [Thomas Güttler]


2.3 (2015-03-19)
----------------
- Bump version 2.3. [Henrique Bastos]
- Readme fix adding syntax highlight for python console. [Henrique Bastos]
- Readme fix adding syntax highlight for python console. [Henrique Bastos]
- Add Csv Helper. [Henrique Bastos]
- Update development dependencies’ versions. [Henrique Bastos]
- Update tox to use python 3.4. [Henrique Bastos]
- Fix annoying error when env lines have non relevant whitespace. [Henrique Bastos]
- Test empty key on ini. [Henrique Bastos]
- Fix #3: return empty string when envvar is empty. [Osvaldo Santana Neto]


2.2 (2015-03-19)
----------------
- Add notice on fail fast policy. [Henrique Bastos]
- Fix boolean convertion of default value. [Henrique Bastos]
- Update setup.py. [Henrique Bastos]
- Update README. [Henrique Bastos]
- Add docutils and pygments to development's requirements.txt. [Henrique Bastos]
- Upgrade development dependencies. [Henrique Bastos]
- Bump version to 2.2. [Henrique Bastos]
- Add badges to README. [Henrique Bastos]
- Fix more landscape reports. [Henrique Bastos]
- Fixing landscape reported issues. [Henrique Bastos]
- Update README. [Henrique Bastos]
- Refactor tests to use fixtures. [Henrique Bastos]
- Fix tests to use Repositories. [Henrique Bastos]
- Adapt AutoConfig to use Repositories with Config. [Henrique Bastos]
- Fix typo. [Henrique Bastos]
- Fix RepositoryEnv logic. [Henrique Bastos]
- Unify Config classes into one. [Henrique Bastos]
- Add comments. [Henrique Bastos]
- Remove unused variables. [Henrique Bastos]
- Add Repository classes. [Henrique Bastos]
- Chage ConfigEnv behavior to raise when option or default are undefined. [Henrique Bastos]


2.1 (2015-03-19)
----------------
- Bump minor version. [Henrique Bastos]
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
- Fix typo. [Henrique Bastos]
- Isolate logic for reading .env. [Henrique Bastos]


2.0 (2015-03-19)
----------------
- Improve README. [Henrique Bastos]
- Add a sample ini to the README. [Henrique Bastos]
- Bump the version. [Henrique Bastos]
- Update and improve README for 2.0. [Henrique Bastos]
- Fix typo. [Henrique Bastos]
- Move exception to a better context. [Henrique Bastos]
- Replace cwd with current module's path. [Henrique Bastos]
- Add a requirements.txt for developers. [Henrique Bastos]
- Implement AutoConfig. [Henrique Bastos]
- Extract the basic API to a base class. [Henrique Bastos]
- Implement ConfigEnv. [Henrique Bastos]
- Add tests to ConfigIni. [Henrique Bastos]
- Make sure to initialize instance attributes. [Henrique Bastos]
- Ignore PyCharm project dir. [Henrique Bastos]
- Add sample INI settings to the README. [Henrique Bastos]


1.0 (2015-03-19)
----------------
- Improve API replacing type with cast. [Henrique Bastos]
- Import code. [Henrique Bastos]
- Add license, readme and setup. [Henrique Bastos]
- Remove old README. [Henrique Bastos]
- Initial commit. [Henrique Bastos]
