from __future__ import absolute_import, unicode_literals
from django.utils import timezone
from celery.schedules import crontab
from .models import Notification
from backend_sl.celery import app
from datetime import datetime, timedelta


# the effect on the database will happen when celery and api containers share same database not sqlite3 different files
@app.task
def delete_expired_notification(*args, **kwargs):
    last_10_days = timezone.now() - timedelta(days=10)
    notifications = Notification.objects.filter(created__lte=last_10_days)
    if notifications:
        notifications.delete()
    return


app.conf.beat_schedule = {
    'delete_expired_notification': {
        'task': 'notification.tasks.delete_expired_notification',
        'schedule': crontab('*/30'),  # each 30 minute check
        # 'args': (16, 16),  # we can pass the task parameters
        # 'kwargs': {},  # we can pass the task keys
    },
}