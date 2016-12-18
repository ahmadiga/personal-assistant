from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone


class Attendance(models.Model):
    user = models.ForeignKey(User)
    check_in = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    check_out = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)

    def check_user_out(self):
        self.check_out = timezone.now()
        self.duration = (self.check_out - self.check_in).total_seconds() * 1000
        self.save()
