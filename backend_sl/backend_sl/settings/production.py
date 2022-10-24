from .base import *


ALLOWED_HOSTS = ['localhost', 'backend-sl'] + list(os.environ.get("DJANGO_ALLOWED_HOSTS").split(" "))




# Postgresql Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),

    }
}

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, '../mediafiles')
STATIC_ROOT = os.path.join(BASE_DIR, '../staticfiles')


# Connect Celery with redis url

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379")
# for put the result in the django data base not in redis
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379")
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

CORS_ALLOW_CREDENTIALS = False


CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]