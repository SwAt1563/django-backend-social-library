from __future__ import absolute_import, unicode_literals
from django.utils import timezone
from datetime import timedelta
from .models import Notification
from backend_sl.celery import app
from datetime import datetime, timedelta
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


# the effect on the database will happen when celery and api containers share same database not sqlite3 different files
@app.task
def delete_expired_notification(*args, **kwargs):
    last_10_days = timezone.now() - timedelta(days=10)
    notifications = Notification.objects.filter(created__lte=last_10_days)
    if notifications:
        count = notifications.count()
        notifications.delete()
        logger.info(f'{count} notifications deleted')
    return 'Notification celery done'


app.conf.beat_schedule.update({
    'delete_expired_notification': {
        'task': 'notification.tasks.delete_expired_notification',
        'schedule': timedelta(minutes=30),  # each 30 minute check
        # 'args': (16, 16),  # we can pass the task parameters
        # 'kwargs': {},  # we can pass the task keys
    },
})