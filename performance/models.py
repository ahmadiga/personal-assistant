from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Performance(models.Model):
    user = models.ForeignKey(User)
    year = models.DateTimeField(default=timezone.now(), null=True, blank=True)
    month = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)
