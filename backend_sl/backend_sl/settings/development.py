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
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379")
# for put the result in the django data base not in redis
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379")
# when we use flower we don't need django_celery_results
if CELERY_RESULT_BACKEND == 'django-db':
    INSTALLED_APPS += ['django_celery_results',]
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Jerusalem'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
REDIS_DB = os.environ.get('REDIS_DB')



#email settings for gmail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("DONOT_REPLY_EMAIL")
DISPLAY_NAME = "Social Library"  # who send the message -name-
# GOOGLE APP PASSWORD
DONOT_REPLY_EMAIL_PASSWORD = os.environ.get("DONOT_REPLY_EMAIL_PASSWORD")


FRONTEND_SITE = 'http://localhost:8000'




# https://github.com/adamchainz/django-cors-headers
# CROS
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True


CORS_ALLOW_METHODS = list(default_methods)
CORS_ALLOW_HEADERS = list(default_headers)



