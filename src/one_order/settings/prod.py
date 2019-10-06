import dj_database_url

from .base import *

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = os.environ.get('HOST')
DATABASES = {
    'default': dj_database_url.config(conn_max_age=600)
}
