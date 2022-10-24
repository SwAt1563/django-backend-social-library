from __future__ import absolute_import, unicode_literals
from django.utils import timezone
from datetime import timedelta
from rest_framework.authtoken.models import Token
from backend_sl.celery import app
from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import get_connection
from account.models import UserAccount

from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task(bind=True)
def create_email(self, user_username: str, **kwargs):

    email_account = kwargs.get("email_account")
    subject = kwargs.get("subject", "")
    email = kwargs.get("email")
    template = kwargs.get("template")
    cc_email = kwargs.get("cc_email")
    context = kwargs.get("context", {})

    context["username"] = user_username
    context['frontend_site'] = settings.FRONTEND_SITE

    email_accounts = {
        "do not reply": {
            'name': settings.EMAIL_HOST_USER,
            'password': settings.DONOT_REPLY_EMAIL_PASSWORD,
            'from': settings.EMAIL_HOST_USER,
            'display_name': settings.DISPLAY_NAME},
    }

    html_content = render_to_string(template, context)  # render with dynamic value
    text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.

    with get_connection(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=email_accounts[email_account]["name"],
            password=email_accounts[email_account]["password"],
            use_tls=settings.EMAIL_USE_TLS,
    ) as connection:
        msg = EmailMultiAlternatives(
            subject,
            text_content,
            f'{email_accounts[email_account]["display_name"]} <{email_accounts[email_account]["from"]}>',
            [email],
            cc=[cc_email], # more emails that you want to send to
            connection=connection)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    return "Done"


# the effect on the database will happen when celery and api containers share same database not sqlite3 different files
@app.task
def delete_expired_tokens(*args, **kwargs):
    last_30_minutes = timezone.now() - timedelta(minutes=30)
    tokens = Token.objects.filter(created__lte=last_30_minutes)
    if tokens:
        count = tokens.count()
        tokens.delete()
        logger.info(f'{count} Tokens deleted')
    return 'Tokens celery Done'


app.conf.beat_schedule.update({
    'delete_expired_tokens': {
        'task': 'account.tasks.delete_expired_tokens',
        'schedule': timedelta(minutes=30),  # each 30 minute check
        # 'args': (16, 16),  # we can pass the task parameters
        # 'kwargs': {},  # we can pass the task keys
    },
})



@app.task
def debug_task(*args, **kwargs):
    logger.info('just for testing every 30 second')
    return 'Celery work'


app.conf.beat_schedule.update({
    'debug_task': {
        'task': 'account.tasks.debug_task',
        'schedule': timedelta(seconds=30),  # each 30 second check
    },
})