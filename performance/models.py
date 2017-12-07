from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Performance(models.Model):
    user = models.ForeignKey(User)
    year = models.IntegerField(null=True)
    month = models.IntegerField(null=True)

    def __str__(self):
        return str(self.user)


class Team(models.Model):
    STATUS_PLANNING = 'PL'
    STATUS_SPRINT = 'SP'
    STATUS_RELEASE = 'RE'
    STATUS_UAT = 'UA'
    STATUS_HANDOVER = 'HO'
    STATUS_CLOSED = 'CL'

    STATUS_CHOICES = (
        (STATUS_PLANNING, 'Planning'),
        (STATUS_SPRINT, 'Sprint'),
        (STATUS_RELEASE, 'Release'),
        (STATUS_UAT, 'UAT'),
        (STATUS_HANDOVER, 'Handover'),
        (STATUS_CLOSED, 'Closed'),
    )

    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User)
    project_name = models.CharField(max_length=255)
    project_length = models.IntegerField(null=True)
    start_project = models.DateField(null=True)
    end_project = models.DateField(null=True)
    status = models.CharField(max_length=2,
                              default=STATUS_PLANNING,
                              choices=STATUS_CHOICES,
                              )
    project_budget = models.FloatField(null=True)
    team_cost_per_hour = models.FloatField(null=True)

    def __str__(self):
        return str(self.name)


class Sprint(models.Model):
    STATUS_PENDING = 'PE'
    STATUS_PLANNING = 'PL'
    STATUS_WORKING = 'WO'
    STATUS_QA = 'QA'
    STATUS_DEPLOY = 'DE'
    STATUS_REVIEW = 'RV'
    STATUS_RETRO = 'RE'
    STATUS_CLOSED = 'CL'

    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_PLANNING, 'Planning'),
        (STATUS_WORKING, 'Working'),
        (STATUS_QA, 'QA'),
        (STATUS_DEPLOY, 'Deploy'),
        (STATUS_REVIEW, 'Review'),
        (STATUS_RETRO, 'Retro'),
        (STATUS_CLOSED, 'Closed'),
    )

    ONEWEEK = 1
    TWOWEEK = 2
    THREEWEEK = 3
    FOURWEEK = 4

    SPRINT_LENGTH_CHOICES = (
        (ONEWEEK, 1),
        (TWOWEEK, 2),
        (THREEWEEK, 3),
        (FOURWEEK, 4),
    )

    name = models.CharField(max_length=255)
    team = models.ForeignKey(Team)
    start_sprint = models.DateField(blank=True)
    end_sprint = models.DateField(blank=True)
    status = models.CharField(max_length=2,
                              default=STATUS_PENDING,
                              choices=STATUS_CHOICES,
                              )
    sprint_length = models.IntegerField(default=ONEWEEK, choices=SPRINT_LENGTH_CHOICES)

    def __str__(self):
        return str(self.name)
