from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.
from django.db.models import Q
from django.utils import timezone
from django.conf import settings

from main.templatetags.calculate_hours import calculate_hours
from main.utils.slack import post_message_on_channel, get_slack_user


class Client(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=255)
    client = models.ForeignKey(Client, blank=True, null=True)
    slack_channel = models.CharField(max_length=255)

    def __str__(self):
        return self.client.name + " - " + self.name


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
    status = models.CharField(max_length=2, default="WA",
                              choices=(("WA", "Waiting"), ("WO", "working"), ("CO", "Completed"),))

    def create_time_entry(self):
        time_entry = TimeEntry.objects.create(title=self.title, description=self.description, project=self.project,
                                              task=self, user=self.submitted_for)


class TimeEntry(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    project = models.ForeignKey(Project, blank=True, null=True)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    task = models.ForeignKey(Task, null=True, blank=True)
    user = models.ForeignKey(User)

    class Meta:
        ordering = ["-started_at", ]

    def __str__(self):
        return self.title

    def recalculate_duration(self):
        self.duration = int((self.ended_at - self.started_at).total_seconds() * 1000)
        self.save()

    def end_time_entry(self):
        if self.ended_at is None:
            self.ended_at = timezone.now()
            self.duration = int((self.ended_at - self.started_at).total_seconds() * 1000)
            self.save()
            if self.task:
                post_message_on_channel(
                    (self.task.project.slack_channel if self.task.project else settings.SLACK_ATTENDANCE_CHANNEL),
                    get_slack_user(
                        self.task.submitted_for) + " finished working on " + get_slack_user(
                        self.task.submitted_by) + "'s request on project " + str(
                        self.task.project) + " with " + self.task.get_priority_display() + " priority after " + calculate_hours(
                        self.duration) + " @ " + str(
                        timezone.localtime(timezone.now()).strftime(
                            "%Y-%m-%d %H:%M")) + "\n for more info please visit " + settings.SITE_URL + str(
                        reverse("user_status", kwargs={"username": self.task.submitted_for})))
            # else:
                # post_message_on_channel(
                #     (self.project.slack_channel if self.project else settings.SLACK_ATTENDANCE_CHANNEL),
                #     get_slack_user(
                #         self.user) + " finished working on \"" + self.title + "\" on project " + str(
                #         self.project) + " after " + calculate_hours(
                #         self.duration) + " @ " + str(
                #         timezone.localtime(timezone.now()).strftime(
                #             "%Y-%m-%d %H:%M")) + "\n for more info please visit " + settings.SITE_URL + str(
                #         reverse("user_status", kwargs={"username": self.user})))

    def stop_running_entries(self):
        active_entry = TimeEntry.objects.filter(Q(Q(user=self.user) & Q(ended_at=None))).first()
        if active_entry:
            active_entry.end_time_entry()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.stop_running_entries()
            self.started_at = timezone.now()
            if self.task:
                post_message_on_channel(
                    (self.task.project.slack_channel if self.task.project else settings.SLACK_ATTENDANCE_CHANNEL),
                    get_slack_user(self.task.submitted_for) + " Start working on " + get_slack_user(
                        self.task.submitted_by) + "'s request on project " + str(
                        self.task.project) + " with " + self.task.get_priority_display() + " priority @ " + str(
                        timezone.localtime(timezone.now()).strftime(
                            "%Y-%m-%d %H:%M")) + "\n for more info please visit " + settings.SITE_URL + str(
                        reverse("user_status", kwargs={"username": self.task.submitted_for})))
            # else:
                # post_message_on_channel(
                #     (self.project.slack_channel if self.project else settings.SLACK_ATTENDANCE_CHANNEL),
                #     get_slack_user(
                #         self.user) + " Start working on \"" + self.title + "\" on project " + str(
                #         self.project) + " @ " + str(
                #         timezone.localtime(timezone.now()).strftime(
                #             "%Y-%m-%d %H:%M")) + "\n for more info please visit " + settings.SITE_URL + str(
                #         reverse("user_status", kwargs={"username": self.user})))

        super(TimeEntry, self).save(*args, **kwargs)
