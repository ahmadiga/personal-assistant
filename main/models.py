from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Profile(models.Model):
    slack_username = models.CharField(max_length=255)
    user = models.OneToOneField(User)
