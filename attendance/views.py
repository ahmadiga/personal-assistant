import logging

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from attendance.forms import AttendanceForm
from attendance.models import Attendance
from main.utils.client_ip import get_client_ip

logger = logging.getLogger('django.channels')

COMPANY_IDS = [
    "185.51.213.81",
    "192.168.99.1",
]


def check_allowed_ips(request):
    client_ip = get_client_ip(request)
    logger.info(client_ip)
    return client_ip in COMPANY_IDS


@login_required
def list_attendance(request, id=None):
    is_allowed = check_allowed_ips(request)
    attendances = Attendance.objects.filter(user=request.user)
    is_checkout = Attendance.objects.filter(check_out=None, user=request.user)
    return render(request, 'attendance/attendance/list_attendance.html',
                  {'attendances': attendances, "is_checkout": is_checkout, "is_allowed": is_allowed})


@login_required
def checkin(request):
    if check_allowed_ips(request):
        attendances = Attendance.objects.create(user=request.user)
    return redirect(reverse('list_attendance'))


@login_required
def checkout(request):
    if check_allowed_ips(request):
        attendance = get_object_or_404(Attendance, check_out=None, user=request.user)
        attendance.check_user_out()
    return redirect(reverse('list_attendance'))


def manage_attendance(request, id=None):
    if id:
        attendance = get_object_or_404(Attendance, pk=id)
    else:
        attendance = None
    form = AttendanceForm(request.POST or None, instance=attendance)
    if form.is_valid():
        form.save()
        return redirect(reverse('list_attendance'))
    return render(request, 'attendance/attendance/manage_attendance.html', {'form': form})


def attendance_details(request, id=None):
    attendance = get_object_or_404(Attendance, pk=id)
    return render(request, 'attendance/attendance/attendance_details.html', {'attendance': attendance})
