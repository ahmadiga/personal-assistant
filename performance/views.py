from django.contrib.auth.decorators import login_required
import datetime
from django.utils import timezone
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, render

from absence.models import Leave
from attendance.models import Attendance
from main.models import MyUser
from time_tracker.models import TimeEntry


@login_required
def performance(request):
    user = request.user
    today = timezone.now()

    # get annual leaves
    min_date = datetime.datetime.utcnow().date().replace(day=1, month=1).isoformat()
    max_date = datetime.datetime.utcnow().date().replace(day=30, month=12).isoformat()
    taken_annual_leave = Leave.objects.filter(type__in=['SL', 'PL'], user=user, pickFrom__gte=min_date, pickFrom__lte=max_date).count()
    total_annual_leave = 14
    remaining_annual_leave = total_annual_leave - taken_annual_leave

    # get monthly hourly leaves
    min_date = datetime.datetime.utcnow().date().replace(day=1).isoformat()
    max_date = datetime.datetime.utcnow().date().replace(day=30).isoformat()
    taken_hourly_leave = Leave.objects.filter(type__in=['TL'], user=user, pickFrom__gte=min_date, pickFrom__lte=max_date).count()
    total_hourly_leave = 12
    remaining_hourly_leave = total_hourly_leave - taken_hourly_leave

    # today performance
    required_hours = 8
    attendance = Attendance.objects.filter(Q(user=user) & Q(check_in__day=today.day) & Q(check_out=None)).first()
    if attendance:
        current_hours = today - attendance.check_in
        current_hours = current_hours.seconds / 60 / 60
        today_performance = int(current_hours / required_hours * 100)
    else:
        current_hours = 0
        current_hours = 0
        today_performance = 0

    # this month performance
    month_required_hours = 176
    month_attendance = Attendance.objects.filter(Q(user=user) & Q(check_in__month=today.month)).aggregate(dsum=Sum("duration"))
    month_current_hours = month_attendance['dsum'] / 1000 / 60 / 60
    month_performance = int(month_current_hours / month_required_hours * 100)


    # this year performance
    year_required_hours = 2112
    year_attendance = Attendance.objects.filter(Q(user=user) & Q(check_in__year=today.year)).aggregate(dsum=Sum("duration"))
    year_current_hours = year_attendance['dsum'] / 1000 / 60 / 60
    year_performance = int(year_current_hours / year_required_hours * 100)

    return render(request, 'performance/performance_dashboard.html',
                  {'taken_annual_leave': taken_annual_leave,
                   'remaining_annual_leave': remaining_annual_leave,
                   'total_annual_leave': total_annual_leave,

                   'taken_hourly_leave': taken_hourly_leave,
                   'remaining_hourly_leave': remaining_hourly_leave,
                   'total_hourly_leave': total_hourly_leave,

                   'required_hours': required_hours,
                   'current_hours': current_hours,
                   'today_performance': today_performance,

                   'month_performance': month_performance,

                   'year_performance': year_performance,
                   })