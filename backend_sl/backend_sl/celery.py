from __future__ import absolute_import, unicode_literals

import os
from celery import Celery
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.environ.get('DJANGO_SETTINGS_MODULE'))
app = Celery('backend_sl')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.timezone = 'Asia/Jerusalem'

app.conf.beat_schedule = {}

'''
For asynchronous tasks 
it will search about tasks in the tasks file in each application
Note: don't forget to import celery in celery/__init__.py file
'''