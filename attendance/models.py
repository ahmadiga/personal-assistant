from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from django.utils import timezone


class Attendance(models.Model):
    user = models.ForeignKey(User)
    check_in = models.DateTimeField(null=True, blank=True, editable=True)
    check_out = models.DateTimeField(null=True, blank=True)
    duration = models.BigIntegerField(null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.check_out:
            self.duration = (self.check_out - self.check_in).total_seconds() * 1000

        super(Attendance, self).save(force_insert, force_update, using, update_fields)

    def check_user_out(self):
        self.check_out = timezone.now()
        self.save()

    def __str__(self):
        return str(self.user) + ' - ' + str(self.check_in)
