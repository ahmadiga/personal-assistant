from __future__ import absolute_import, unicode_literals
import os

import datetime

import pymysql
from celery import Celery
from celery.utils.log import get_task_logger
# set the default Django settings module for the 'celery' program.
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.utils import timezone
from main.utils.slack import post_message_on_channel, get_slack_user

pymysql.install_as_MySQLdb()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'personal_assistant.common')

app = Celery('personal_assistant')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

logger = get_task_logger(__name__)


@app.task
def did_not_check_in():
    from attendance.models import Attendance
    today_date = datetime.datetime.utcnow().date()
    today_date = datetime.datetime(today_date.year, today_date.month, today_date.day)
    entries = Attendance.objects.filter(
        Q(Q(
            Q(check_in__gt=today_date))))
    result = ""
    for entry in entries:
        result = get_slack_user(entry.user)

    if result:
        post_message_on_channel(settings.SLACK_ATTENDANCE_CHANNEL,
                                result + " did you forget to check in! if so please go to " + settings.SITE_URL + str(
                                    reverse("list_attendance")))


@app.task
def did_not_start_timer():
    from django.contrib.auth.models import User
    today_date = datetime.datetime.utcnow().date()
    today_date = datetime.datetime(today_date.year, today_date.month, today_date.day)
    lastHourDateTime = timezone.now() - datetime.timedelta(hours=1)
    users = User.objects.filter(
        Q(
            Q(
                Q(attendance__check_in__gt=today_date) &
                Q(attendance__check_out=None)
            ) &
            Q(
                ~Q(timeentry__ended_at=None) &
                ~Q(timeentry__ended_at__gt=lastHourDateTime)
            )
        )
    )
    result = ""
    for user in users:
        result = get_slack_user(user)
    print(lastHourDateTime.strftime('%Y-%m-%d %H:%M:%S'))
    if result:
        post_message_on_channel(settings.SLACK_ATTENDANCE_CHANNEL,
                                result + " did you forget to start your timer! if so please go to " + settings.SITE_URL + str(
                                    reverse("list_timeentry")))
