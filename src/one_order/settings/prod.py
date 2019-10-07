import dj_database_url

from .base import *

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = os.environ.get('HOST')
DATABASES = {
    'default': dj_database_url.config(conn_max_age=600)
}

MIDDLEWARE += [
    'baipw.middleware.BasicAuthIPWhitelistMiddleware'
]
BASIC_AUTH_LOGIN = os.environ.get('USER_ROLE')
BASIC_AUTH_PASSWORD = os.environ.get('USER_PASS')
