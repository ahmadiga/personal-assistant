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

pymysql.install_as_MySQLdb()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_starterkit.common')

app = Celery('django_starterkit')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

logger = get_task_logger(__name__)


@app.task
def test():
    logger.info("test task")
