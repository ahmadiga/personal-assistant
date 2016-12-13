from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=255)
    toggl_id = models.CharField(max_length=255)
    client = models.CharField(max_length=255)
    slack_channel = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=2,
                                choices=(("UR", "Urgent"), ("HI", "High"), ("ME", "Medium"), ("LO", "Low"),))
    estimated_time = models.DurationField(null=True, blank=True)
    project = models.ForeignKey(Project)
    submitted_by = models.ForeignKey(User, related_name="submitted_by")
    create_date = models.DateTimeField(auto_now_add=True)
    submitted_for = models.ForeignKey(User, related_name="submitted_for")
    time_entry_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=2, default="WA",
                              choices=(("WA", "Waiting"), ("WO", "working"), ("CO", "Completed"),))
