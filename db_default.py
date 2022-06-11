from decouple import config
from dj_database_url import parse as db_url

# BASE_DIR, config('DEBUG'), custome name for default sqlite3 database, linking database url link
def db_default(base_dir, debug, default_database_name, database_url):
    if debug:
        return {'default' :{
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': base_dir / f'{default_database_name}.sqlite3',
        }}
    else:
        return {'default':config(database_url, cast=db_url)}
