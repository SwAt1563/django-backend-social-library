from __future__ import absolute_import, unicode_literals
from django.utils import timezone
from celery.schedules import crontab
from rest_framework.authtoken.models import Token
from backend_sl.celery import app
from datetime import datetime, timedelta


# the effect on the database will happen when celery and api containers share same database not sqlite3 different files
@app.task
def delete_expired_tokens(*args, **kwargs):
    last_1_hour = timezone.now() - timedelta(hours=1)
    tokens = Token.objects.filter(created__lte=last_1_hour)
    if tokens:
        tokens.delete()
    return


app.conf.beat_schedule = {
    'delete_expired_tokens': {
        'task': 'notification.tasks.delete_expired_tokens',
        'schedule': crontab('*/30'),  # each 30 minute check
        # 'args': (16, 16),  # we can pass the task parameters
        # 'kwargs': {},  # we can pass the task keys
    },
}