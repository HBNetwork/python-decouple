# coding: utf-8
import pytest
from decouple import Config, Csv


def test_csv():
    csv = Csv()
    assert ['127.0.0.1', '.localhost', '.herokuapp.com'] == \
        csv('127.0.0.1, .localhost, .herokuapp.com')

    csv = Csv(int)
    assert [1, 2, 3, 4, 5] == csv('1,2,3,4,5')

    csv = Csv(post_process=tuple)
    assert ('HTTP_X_FORWARDED_PROTO', 'https') == \
        csv('HTTP_X_FORWARDED_PROTO, https')

    csv = Csv(cast=lambda s: s.upper(), delimiter='\t', strip=' %*')
    assert ['VIRTUAL_ENV', 'IMPORTANT STUFF', 'TRAILING SPACES'] == \
        csv('%virtual_env%\t *important stuff*\t   trailing spaces   ')


def test_csv_quoted_parse():
    csv = Csv()

    assert ['foo', 'bar, baz', 'qux'] == csv(""" foo ,'bar, baz', 'qux'""")

    assert ['foo', 'bar, baz', 'qux'] == csv(''' foo ,"bar, baz", "qux"''')

    assert ['foo', "'bar, baz'", "'qux"] == csv(''' foo ,"'bar, baz'", "'qux"''')

    assert ['foo', '"bar, baz"', '"qux'] == csv(""" foo ,'"bar, baz"', '"qux'""")


def test_csv_none():
    csv = Csv()
    assert [] == csv(None)


@pytest.mark.parametrize('value', [None, ''])
@pytest.mark.parametrize('post_process, expected', [
    (list, []), (tuple, ()), (sum, 0), (sorted, []),
])
def test_csv_empty_post_process(value, post_process, expected):
    csv = Csv(cast=int, post_process=post_process)
    assert expected == csv(value)


def test_csv_none_default_with_custom_post_process(monkeypatch):
    monkeypatch.delenv('CSV_OPTION', raising=False)

    def post_process(values):
        return next(values, 'empty')

    csv = Csv(cast=pytest.fail, post_process=post_process)
    config = Config({})
    assert 'empty' == config('CSV_OPTION', default=None, cast=csv)
