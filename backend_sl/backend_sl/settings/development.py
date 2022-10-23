from .base import *
from corsheaders.defaults import default_methods, default_headers

# open the website from localhost
# make request on the backend-sl container
ALLOWED_HOSTS = ['localhost', 'backend-sl']
# Sqlite Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / '../db.sqlite3',
    },
    'test_db': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / '../test_db.sqlite3',
    }
}

STATIC_URL = 'static/'
MEDIA_URL = 'media/'

MEDIA_ROOT = os.path.join(BASE_DIR, '../media')
STATIC_ROOT = os.path.join(BASE_DIR, '../static')


# Connect Celery with redis url
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')
CELERY_TIMEZONE = 'Asia/Jerusalem'

REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
REDIS_DB = os.environ.get('REDIS_DB')



# https://github.com/adamchainz/django-cors-headers

# who can use my api
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True


CORS_ALLOW_METHODS = list(default_methods)
CORS_ALLOW_HEADERS = list(default_headers)



