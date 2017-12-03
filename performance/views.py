from django.contrib.auth.decorators import login_required
import datetime
from django.utils import timezone
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, render

from absence.models import Leave
from attendance.models import Attendance
from attendance.views import check_allowed_ips
from main.models import MyUser
from performance.models import Team
from time_tracker.models import TimeEntry


@login_required
def performance(request):
    user = request.user
    today = timezone.now()
    is_checkout = Attendance.objects.filter(check_out=None, user=user)


    # get annual leaves
    year_min_date = datetime.datetime.utcnow().date().replace(day=1, month=1).isoformat()
    year_max_date = datetime.datetime.utcnow().date().replace(day=1, month=12).isoformat()
    taken_annual_leave = Leave.objects.filter(type__in=['SL', 'PL'], user=user,
                                              pickFrom__gte=year_min_date, pickFrom__lte=year_max_date).count()
    total_annual_leave = 14
    remaining_annual_leave = total_annual_leave - taken_annual_leave

    # get monthly hourly leaves
    month_min_date = datetime.datetime.utcnow().date().replace(day=1).isoformat()
    month_max_date = datetime.datetime.utcnow().date().replace(day=30).isoformat()

    taken_hourly_leave = Leave.objects.filter(type__in=['TL'], user=user,
                                              pickFrom__gte=month_min_date, pickFrom__lte=month_max_date).count()
    total_hourly_leave = 12
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
    month_max_date = datetime.datetime.utcnow().date().replace(day=30).isoformat()
    monthly_taken_hourly_leave = Leave.objects.filter(
        type__in=['TL'], user=user, pickFrom__gte=month_min_date, pickFrom__lte=month_max_date).count()
    monthly_taken_leave = Leave.objects.filter(
        type__in=['SL', 'PL'], user=user, pickFrom__gte=month_min_date, pickFrom__lte=month_max_date).count()
    month_required_hours = 176 - (monthly_taken_hourly_leave * 3) - (monthly_taken_leave * 8)
    month_attendance = Attendance.objects.filter(
        Q(user=user) & Q(check_in__month=today.month)).aggregate(dsum=Sum("duration"))
    if attendance:
        month_current_hours = month_attendance['dsum'] / 1000 / 60 / 60
        month_performance = int(month_current_hours / month_required_hours * 100)
    else:
        month_current_hours = 0
        month_performance = 0


    # this year performance
    year_min_date = datetime.datetime.utcnow().date().replace(day=1, month=1).isoformat()
    year_max_date = datetime.datetime.utcnow().date().replace(day=1, month=12).isoformat()
    yearly_taken_hourly_leave = Leave.objects.filter(
        type__in=['TL'], user=user, pickFrom__gte=year_min_date, pickFrom__lte=year_max_date).count()
    yearly_taken_leave = Leave.objects.filter(
        type__in=['SL', 'PL'], user=user, pickFrom__gte=year_min_date, pickFrom__lte=year_max_date).count()
    year_required_hours = 2112 - (yearly_taken_hourly_leave * 3) - (yearly_taken_leave * 8)
    year_attendance = Attendance.objects.filter(
        Q(user=user) & Q(check_in__year=today.year)).aggregate(dsum=Sum("duration"))
    year_current_hours = year_attendance['dsum'] / 1000 / 60 / 60
    year_performance = int(year_current_hours / year_required_hours * 100)

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
    return render(request, 'performance/team_performance_dashboard.html', {'team': team})