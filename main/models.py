from __future__ import unicode_literals

import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q


# Create your models here.


class Profile(models.Model):
    slack_username = models.CharField(max_length=255)
    user = models.OneToOneField(User)


class MyUser(User):
    class Meta:
        proxy = True

    def get_todat_timeentry(self, today_date):
        return self.timeentry_set.filter(
            Q(~Q(ended_at=None) & Q(
                Q(started_at__gt=today_date) & Q(started_at__lt=today_date + datetime.timedelta(days=1)))))

    def get_today_timeentry(self):
        return self.timeentry_set.filter(Q(ended_at=None)).first()

    def did_attended_today(self):
        today_date = datetime.datetime.utcnow().date()
        today_date = datetime.datetime(today_date.year, today_date.month, today_date.day)
        return True if self.attendance_set.filter(check_in__gte=today_date, check_out=None) else False
