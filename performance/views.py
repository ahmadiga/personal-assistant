import logging

from django.contrib.auth.decorators import login_required
import datetime
from django.utils import timezone
from django.db.models import Q, Sum, Avg
from django.shortcuts import get_object_or_404, render

from absence.models import Leave
from attendance.models import Attendance
from attendance.views import check_allowed_ips
from main.models import MyUser
from performance.models import Team, Sprint
from time_tracker.models import TimeEntry

logger = logging.getLogger('django.channels')


@login_required
def performance(request):
    if datetime.datetime.utcnow().date().month == 2:
        try:
            this_month_max_day = datetime.datetime.utcnow().date().replace(day=29).isoformat()
        except:
            this_month_max_day = datetime.datetime.utcnow().date().replace(day=28).isoformat()
    else:
        try:
            this_month_max_day = datetime.datetime.utcnow().date().replace(day=31).isoformat()
        except:
            this_month_max_day = datetime.datetime.utcnow().date().replace(day=30).isoformat()

    user = request.user
    today = timezone.now()
    is_checkout = Attendance.objects.filter(check_out=None, user=user)

    # get annual leaves
    year_min_date = datetime.datetime.utcnow().date().replace(day=1, month=1).isoformat()
    year_max_date = datetime.datetime.utcnow().date().replace(day=31, month=12).isoformat()
    taken_annual_leave = Leave.objects.filter(type__in=['SL', 'PL'], user=user,
                                              pickFrom__gte=year_min_date, pickFrom__lte=year_max_date).count()
    total_annual_leave = 14
    remaining_annual_leave = total_annual_leave - taken_annual_leave

    # get monthly hourly leaves
    month_min_date = datetime.datetime.utcnow().date().replace(day=1).isoformat()
    month_max_date = this_month_max_day

    total_hourly_leave = 12
    temp_leaves = Leave.objects.filter(type__in=['TL'], user=user,
                                       pickFrom__gte=month_min_date, pickFrom__lte=month_max_date)
    taken_hourly_leave = temp_leaves.count()

    for temp_leave in temp_leaves:
        duration = temp_leave.pickTo - temp_leave.pickFrom
        taken_hourly_leave += (duration.seconds / 60 / 60)

    remaining_hourly_leave = total_hourly_leave - taken_hourly_leave

    # today performance
    day_min_date = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0).isoformat()
    day_max_date = datetime.datetime.utcnow().replace(hour=23, minute=59, second=59).isoformat()
    daily_taken_hourly_leave = Leave.objects.filter(type__in=['TL'], user=user,
                                                    pickFrom__gte=day_min_date, pickFrom__lte=day_max_date).count()
    required_hours = 8 - (daily_taken_hourly_leave * 3)
    attendance = Attendance.objects.filter(Q(user=user) & Q(check_in__day=today.day)
                                           & Q(check_out=None)).first()
    if attendance:
        current_hours = today - attendance.check_in
        current_hours = current_hours.seconds / 60 / 60
        today_performance = int(current_hours / required_hours * 100)
    else:
        current_hours = 0
        today_performance = 0

    # this month performance
    month_min_date = datetime.datetime.utcnow().date().replace(day=1).isoformat()
    month_max_date = this_month_max_day
    monthly_taken_hourly_leave = Leave.objects.filter(
        type__in=['TL'], user=user, pickFrom__gte=month_min_date, pickFrom__lte=month_max_date).count()
    monthly_taken_leave = Leave.objects.filter(
        type__in=['SL', 'PL'], user=user, pickFrom__gte=month_min_date, pickFrom__lte=month_max_date).count()
    month_required_hours = 176 - (monthly_taken_hourly_leave * 3) - (monthly_taken_leave * 8)
    month_attendance = Attendance.objects.filter(
        Q(user=user) & Q(check_in__month=today.month)).aggregate(dsum=Sum("duration"))

    if month_attendance and month_attendance['dsum']:
        month_current_hours = month_attendance['dsum'] / 1000 / 60 / 60
        month_performance = int(month_current_hours / month_required_hours * 100)
    else:
        month_performance = 0

    # this year performance
    year_min_date = datetime.datetime.utcnow().date().replace(day=1, month=1).isoformat()
    year_max_date = datetime.datetime.utcnow().date().replace(day=31, month=12).isoformat()
    yearly_taken_hourly_leave = Leave.objects.filter(
        type__in=['TL'], user=user, pickFrom__gte=year_min_date, pickFrom__lte=year_max_date).count()
    yearly_taken_leave = Leave.objects.filter(
        type__in=['SL', 'PL'], user=user, pickFrom__gte=year_min_date, pickFrom__lte=year_max_date).count()
    year_required_hours = 2112 - (yearly_taken_hourly_leave * 3) - (yearly_taken_leave * 8)
    year_attendance = Attendance.objects.filter(
        Q(user=user) & Q(check_in__year=today.year)).aggregate(dsum=Sum("duration"))

    if year_attendance and year_attendance['dsum']:
        year_current_hours = year_attendance['dsum'] / 1000 / 60 / 60
        year_performance = int(year_current_hours / year_required_hours * 100)
    else:
        year_performance = 0

    return render(request, 'performance/performance_dashboard.html',
                  {'is_checkout': is_checkout,

                   'taken_annual_leave': taken_annual_leave,
                   'remaining_annual_leave': remaining_annual_leave,
                   'total_annual_leave': total_annual_leave,

                   'taken_hourly_leave': taken_hourly_leave,
                   'remaining_hourly_leave': remaining_hourly_leave,
                   'total_hourly_leave': total_hourly_leave,

                   'required_hours': required_hours,
                   'current_hours': current_hours,
                   'today_performance': today_performance,
                   'daily_taken_hourly_leave': daily_taken_hourly_leave,

                   'month_performance': month_performance,
                   'monthly_taken_hourly_leave': monthly_taken_hourly_leave,

                   'year_performance': year_performance,
                   'yearly_taken_hourly_leave': yearly_taken_hourly_leave,
                   })


@login_required
def team_performance(request):
    teams = Team.objects.filter(users=request.user)

    return render(request, 'performance/list_team.html', {'teams': teams})


def team_performance_dashboard(request, id=None):
    team = get_object_or_404(Team, pk=id)
    sprint = Sprint.objects.get(~Q(status='PE') & Q(team=team))
    all_sprints = team.sprint_set.all()
    members = team.users.all()

    # sprint performance ------------start-----------
    sprint_required_hours = sprint.sprint_length * 5 * 8 * members.count()
    team_actual_hours = 0

    for member in members:
        mil_seconds = Attendance.objects.filter(
            Q(user=member) & Q(check_in__gte=sprint.start_sprint) & Q(check_in__lte=sprint.end_sprint)).aggregate(
            dsum=Sum("duration"))['dsum']
        if mil_seconds:
            team_actual_hours += (mil_seconds / 1000 / 60 / 60)

    sprint_performance = int((team_actual_hours / sprint_required_hours) * 100)
    # sprint performance ------------end-----------

    # project performance ------------start-----------
    project_required_hours = team.project_length * 5 * 8 * members.count()
    project_team_actual_hours = 0

    for member in members:
        mil_seconds = Attendance.objects.filter(
            Q(user=member) & Q(check_in__gte=team.start_project) & Q(check_in__lte=team.end_project)).aggregate(
            dsum=Sum("duration"))['dsum']
        if mil_seconds:
            project_team_actual_hours += (mil_seconds / 1000 / 60 / 60)

    project_performance = int((project_team_actual_hours / project_required_hours) * 100)
    # project performance -----------end------------

    # project budget ------------start-----------
    team_cost = team.team_cost_per_hour * team.project_length * 5 * 8
    project_budget = team.project_budget

    budget_performance = team_cost / project_budget
    # project budget -------------end----------

    # team member performance ----------start----------
    members_performance = []
    for member in members:
        duration_sum = Attendance.objects.filter(
            Q(user=member) & Q(check_in__gte=team.start_project) & Q(check_in__lte=team.end_project)).aggregate(
            dsum=Sum("duration"))['dsum']
        if duration_sum:
            duration_sum = (duration_sum / 1000 / 60 / 60)
        else:
            duration_sum = 0
        temp = {}
        temp['profile'] = member
        temp['result'] = int(duration_sum)



        average_check_in = Attendance.objects.filter(
            Q(user=member) & Q(check_in__gte=team.start_project) & Q(check_in__lte=team.end_project)& ~Q(check_out=None)).order_by('-id')
        average_check_out = Attendance.objects.filter(
            Q(user=member) & Q(check_in__gte=team.start_project) & Q(check_in__lte=team.end_project) & ~Q(check_out=None)).order_by('-id')

        if average_check_in.exists() and average_check_out.exists():
            temp['check_in'] = float(average_check_in[0].check_in.strftime('%H.%M'))
            temp['check_out'] = float(average_check_out[0].check_out.strftime('%H.%M')) - temp['check_in']
            temp['check_final'] = 16 - temp['check_out']
        else:
            temp['check_in'] = 0
            temp['check_out'] = 0
            temp['check_final'] = 24

        members_performance.append(temp)
    #  team member performance ----------end-------


    return render(request, 'performance/team_performance_dashboard.html',
                  {
                      'team': team,
                      'sprint': sprint,
                      'members': members,
                      'all_sprints': all_sprints,

                      'sprint_performance': sprint_performance,
                      'project_performance': project_performance,
                      'budget_performance': budget_performance,

                      'members_performance': members_performance,

                  })
