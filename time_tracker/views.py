import logging
from collections import OrderedDict

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings

# Create your views here.
from attendance.models import Attendance
from main.templatetags.time_from import time_from
from main.utils.slack import post_message_on_channel, get_slack_user
from time_tracker.forms import ClientForm, ProjectForm, TimeEntryForm, TaskForm
from time_tracker.models import Client, Project, TimeEntry, Task
import datetime
from django.utils import timezone

logger = logging.getLogger('django.channels')


def list_client(request, id=None):
    clients = Client.objects.all()
    return render(request, 'time_tracker/client/list_client.html', {'clients': clients})


def manage_client(request, id=None):
    if id:
        client = get_object_or_404(Client, pk=id)
    else:
        client = None
    form = ClientForm(request.POST or None, instance=client)
    if form.is_valid():
        form.save()
        return redirect(reverse('list_client'))
    return render(request, 'time_tracker/client/manage_client.html', {'form': form})


def client_details(request, id=None):
    client = get_object_or_404(Client, pk=id)
    return render(request, 'time_tracker/client/client_details.html', {'client': client})


def list_project(request, id=None):
    projects = Project.objects.all()
    return render(request, 'time_tracker/project/list_project.html', {'projects': projects})


def manage_project(request, id=None):
    if id:
        project = get_object_or_404(Project, pk=id)
    else:
        project = None
    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        return redirect(reverse('list_project'))
    return render(request, 'time_tracker/project/manage_project.html', {'form': form})


def project_details(request, id=None):
    project = get_object_or_404(Project, pk=id)
    return render(request, 'time_tracker/project/project_details.html', {'project': project})


@login_required
def list_timeentry(request, id=None):
    today_date = timezone.now().date()
    today_date = datetime.datetime(today_date.year, today_date.month, today_date.day)
    timeentrys = TimeEntry.objects.filter(
        Q(
            Q(user=request.user) &
            ~Q(ended_at=None) &
            Q(started_at__gt=today_date - datetime.timedelta(days=7))
        )
    ).extra(select={'day': 'date(started_at)'})
    output = OrderedDict()
    for timeentry in timeentrys:
        logger.info(output)
        if timeentry.day not in output:
            output[timeentry.day] = {
                "items": [],
                "total": 0
            }
        output[timeentry.day]["items"].append(timeentry)
        output[timeentry.day]["total"] += timeentry.duration

    active_entry = TimeEntry.objects.filter(Q(Q(user=request.user) & Q(ended_at=None))).first()
    if active_entry and today_date.date() in output:
        output[today_date.date()]["total"] += time_from(active_entry.started_at)
    return render(request, 'time_tracker/timeentry/list_timeentry.html',
                  {'output': output, "active_entry": active_entry, "today_date": today_date.date()})


@login_required
def manage_timeentry(request, id=None):
    if id:
        timeentry = get_object_or_404(TimeEntry, pk=id)
    else:
        timeentry = None
    form = TimeEntryForm(request.POST or None, instance=timeentry)
    if form.is_valid():
        form.instance.user = request.user
        form.save()
        return redirect(reverse('list_timeentry'))
    return render(request, 'time_tracker/timeentry/manage_timeentry.html', {'form': form})


@login_required
def timeentry_details(request, id=None):
    timeentry = get_object_or_404(TimeEntry, pk=id)
    return render(request, 'time_tracker/timeentry/timeentry_details.html', {'timeentry': timeentry})


@login_required
def end_entry(request):
    entry = get_object_or_404(TimeEntry, ended_at=None, user=request.user)
    entry.end_time_entry()
    return redirect(reverse('list_timeentry'))


def list_task(request, id=None):
    tasks = Task.objects.all()
    return render(request, 'time_tracker/task/list_task.html', {'tasks': tasks})


@login_required
def manage_task(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user

    is_checkin = Attendance.objects.filter(check_out=None, user=user)
    form = TaskForm(request.POST or None, user=user)
    if form.is_valid():
        form.instance.submitted_by = request.user
        form.instance.submitted_for = user
        form.save()
        post_message_on_channel(
            (form.instance.project.slack_channel if form.instance.project else settings.SLACK_ATTENDANCE_CHANNEL),
            get_slack_user(
                request.user) + " submitted a " + form.instance.get_priority_display() + " priority request to " + get_slack_user(
                user) + " on project " + str(form.instance.project.name) + " @ " + str(
                timezone.localtime(timezone.now()).strftime(
                    "%Y-%m-%d %H:%M")) + "\n for more info please visit" + str(
                request.build_absolute_uri(
                    reverse("user_status", kwargs={"username": user.username}))))
        if user == request.user:
            return redirect(reverse('dashboard'))
        else:
            return redirect(reverse('user_status', kwargs={"username": user.username}))
    return render(request, 'time_tracker/task/manage_task.html', {'form': form, "is_checkin": is_checkin})


def task_details(request, id=None):
    task = get_object_or_404(Task, pk=id)
    return render(request, 'time_tracker/task/task_details.html', {'task': task})


def create_task(request, id):
    task = get_object_or_404(Task, pk=id)
    task.create_time_entry()
    task.status = "WO"
    task.save()
    return redirect(reverse('dashboard'))


def stop_task(request, id):
    task = get_object_or_404(Task, pk=id)
    for entry in task.timeentry_set.all():
        entry.end_time_entry()
    task.status = "CO"
    task.save()
    return redirect(reverse('dashboard'))
