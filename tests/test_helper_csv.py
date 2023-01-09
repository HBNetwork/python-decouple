# coding: utf-8
from decouple import Csv


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
