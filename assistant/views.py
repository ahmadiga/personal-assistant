from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from assistant.forms import TaskForm, ProjectForm
from assistant.models import Task, Project
from attendance.models import Attendance
from main.utils.toggl import Toggl


def list_task(request, id=None):
    tasks = Task.objects.all()
    return render(request, 'assistant/task/list_task.html', {'tasks': tasks})


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
        if user == request.user:
            return redirect(reverse('dashboard'))
        else:
            return redirect(reverse('user_status', kwargs={"username": user.username}))
    return render(request, 'assistant/task/manage_task.html', {'form': form, "is_checkin": is_checkin})


def task_details(request, id=None):
    task = get_object_or_404(Task, pk=id)
    return render(request, 'assistant/task/task_details.html', {'task': task})


def create_toggl_task(request, id):
    task = get_object_or_404(Task, pk=id)
    toggl = Toggl(request.user.profile.toggl_token)
    data = toggl.create_start_time_entry(task)
    task.status = "WO"
    task.time_entry_id = data["id"]
    task.save()
    return redirect(reverse('dashboard'))


def stop_toggl_task(request, id):
    task = get_object_or_404(Task, pk=id)
    toggl = Toggl(request.user.profile.toggl_token)
    data = toggl.stop_time_entry(task.time_entry_id)
    task.status = "CO"
    task.save()
    return redirect(reverse('dashboard'))


def list_project(request, id=None):
    projects = Project.objects.filter(user=request.user)
    return render(request, 'assistant/project/list_project.html', {'projects': projects})


def manage_project(request, id=None):
    if id:
        project = get_object_or_404(Project, pk=id)
    else:
        project = None
    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        return redirect(reverse('list_project'))
    return render(request, 'assistant/project/manage_project.html', {'form': form})


def project_details(request, id=None):
    project = get_object_or_404(Project, pk=id)
    return render(request, 'assistant/project/project_details.html', {'project': project})
