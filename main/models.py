from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from assistant.models import Project
from main.utils.toggl import Toggl


class Profile(models.Model):
    slack_token = models.CharField(max_length=255)
    toggl_token = models.CharField(max_length=255)
    user = models.OneToOneField(User)

    def update_projects(self):
        toggl = Toggl(self.toggl_token)
        projects = toggl.get_projects()
        # Project.objects.filter(user=self.user).delete()
        for project in projects:
            Project.objects.get_or_create(toggl_id=project["id"], user=self.user,
                                          defaults={"name": project["name"], "client": project["client"]})
