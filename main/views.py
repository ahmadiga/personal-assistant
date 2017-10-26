import datetime
import logging

from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.db.models import Q, Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.dateparse import parse_date
from django.utils.timezone import make_aware, get_current_timezone
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from attendance.models import Attendance
from main.forms import ProfileForm
from main.models import Profile, MyUser
from time_tracker.models import TimeEntry, Task, Project

logger = logging.getLogger('django.channels')


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    if request.user.is_authenticated():
        return redirect(reverse("home"))

    redirect_to = request.GET.get(redirect_field_name, '/')

    form = authentication_form(request, data=request.POST or None)
    if form.is_valid():
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        auth_login(request, form.get_user())
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
        return redirect(redirect_to)

    request.session.set_test_cookie()

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template_name, context)


# server_1    | [{'channel': 'D1HC3F41E', 'team': 'T02UE0HBX', 'user': 'U02UHRR5A', 'type': 'message', 'ts': '1481467353.000004', 'text': 'test'}]

# server_1    | [{'channel': 'D0B22214H', 'team': 'T02UE0HBX', 'text': 'asd', 'type': 'message', 'user': 'U0A8VQ9EF', 'ts': '1481465397.000014'}]
# server_1    | {'user': 'U02UHRR5A', 'channel': 'G0441SCJN', 'ts': '1481469188.000021', 'type': 'message', 'team': 'T02UE0HBX', 'text': 'test'}

# Create your views here.
@login_required
def dashboard(request, username=None):
    if username:
        user = get_object_or_404(MyUser, username=username)
        dashboard = False
    else:
        user = get_object_or_404(MyUser, pk=request.user.pk)
        dashboard = True
    if "date" in request.GET:
        today_date = parse_date(request.GET["date"])
    else:
        today_date = datetime.datetime.utcnow().date()
    today_date = datetime.datetime(today_date.year, today_date.month, today_date.day)
    today_date = make_aware(today_date, get_current_timezone(), is_dst=False)
    active_entry = user.get_today_timeentry()
    entries = user.get_todat_timeentry(today_date)
    entries_totals = Project.objects.values('name', 'client__name').filter(
        Q(Q(timeentry__user=user) & Q(
            Q(timeentry__started_at__gt=today_date) & Q(
                timeentry__started_at__lt=today_date + datetime.timedelta(days=1))))).annotate(
        dsum=Sum("timeentry__duration"))
    today_totals = TimeEntry.objects.filter(
        Q(Q(user=user) & Q(
            Q(started_at__gt=today_date) & Q(started_at__lt=today_date + datetime.timedelta(days=1))))).aggregate(
        Sum("duration"))
    week_totals = TimeEntry.objects.filter(
        Q(Q(user=user) & Q(
            Q(started_at__lt=today_date) & Q(started_at__gt=today_date - datetime.timedelta(days=7))))).aggregate(
        Sum("duration"))
    if today_totals and "duration__sum" in today_totals and today_totals["duration__sum"]:
        today_totals = today_totals["duration__sum"]
    else:
        today_totals = 0
    if week_totals and "duration__sum" in week_totals and week_totals["duration__sum"]:
        week_totals = int(week_totals["duration__sum"] / 5)
    else:
        week_totals = 0
    attendance = Attendance.objects.filter(user=user).last()
    queue_tasks = Task.objects.filter(Q(Q(submitted_for=user) & Q(Q(status="WA") | Q(status="WO"))))

    return render(request, 'main/dashboard/dashboard.html', {
        "active_task": active_entry,
        "today_tasks": entries,
        "queue_tasks": queue_tasks,
        "dashboard": dashboard,
        "user": user,
        "attendance": attendance,
        "entries_totals": entries_totals,
        "today_totals": today_totals,
        "week_totals": week_totals,
        "today_date": today_date,
    })


def index(request):
    if request.user.is_authenticated():
        return redirect(reverse("dashboard"))
    return render(request, 'main/index.html', {})


def manage_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    form = ProfileForm(request.POST or None, instance=profile)
    if form.is_valid():
        form.instance.save()
        return redirect(reverse('dashboard'))
    return render(request, 'main/profile/manage_profile.html', {'form': form})


def profile_details(request, id=None):
    profile = get_object_or_404(Profile, pk=id)
    return render(request, 'main/profile/profile_details.html', {'profile': profile})


def list_profile(request):
    profiles = MyUser.objects.all()
    return render(request, 'main/profile/list_profile.html', {'profiles': profiles})


def update_projects(request):
    if hasattr(request.user, "profile") and request.user.profile.toggl_token:
        request.user.profile.update_projects()
    return redirect(reverse("list_project"))
