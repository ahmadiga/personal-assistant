import logging

import datetime
import xlwt
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.
from django.utils import timezone

from attendance.forms import AttendanceForm, AttendanceFilter
from attendance.models import Attendance
from main.templatetags.calculate_hours import calculate_hours
from main.utils.client_ip import get_client_ip
from main.utils.slack import post_message_on_channel, get_slack_user

logger = logging.getLogger('django.channels')

COMPANY_IDS = [
    "185.51.213.81",
    "192.168.99.1",
]


def check_allowed_ips(request):
    client_ip = get_client_ip(request)
    logger.info(client_ip)
    # return client_ip in COMPANY_IDS
    return True

@login_required
def list_attendance(request, id=None):
    is_allowed = check_allowed_ips(request)

    attendances = Attendance.objects.filter(user=request.user).order_by('-check_in')
    is_checkout = Attendance.objects.filter(check_out=None, user=request.user)

    f = AttendanceFilter(request.GET, queryset=attendances)
    if request.GET.get("excel", False):
        return export_attendance_xls(f.qs)
    else:
        # Pagination
        page = request.GET.get('page', 1)
        paginator = Paginator(f.qs, 10)
        try:
            attendances = paginator.page(page)
        except PageNotAnInteger:
            attendances = paginator.page(1)
        return render(request, 'attendance/attendance/list_attendance.html',
                      {'attendances': attendances, "is_checkout": is_checkout, "is_allowed": is_allowed, 'filter': f})

@login_required
def checkin(request):
    if check_allowed_ips(request):
        if not Attendance.objects.filter(check_out=None, user=request.user):
            attendances = Attendance.objects.create(user=request.user, check_in=timezone.now())
            post_message_on_channel(settings.SLACK_ATTENDANCE_CHANNEL,
                                    get_slack_user(request.user) + " checked in at SIT office @ " + str(
                                        timezone.localtime(timezone.now()).strftime(
                                            "%Y-%m-%d %H:%M")) + "\n for more info please visit" + settings.SITE_URL + str(
                                        reverse("user_status", kwargs={"username": request.user.username})))
    return redirect(reverse('list_attendance'))


@login_required
def checkout(request):
    if check_allowed_ips(request):
        attendance = get_object_or_404(Attendance, check_out=None, user=request.user)
        attendance.check_user_out()
        post_message_on_channel(settings.SLACK_ATTENDANCE_CHANNEL,
                                get_slack_user(request.user) + " checked out from SIT office @ " + str(
                                    timezone.localtime(
                                        timezone.now()).strftime("%Y-%m-%d %H:%M")) + "\n duration: " + calculate_hours(
                                    int(
                                        attendance.duration)) + "\n for more info please visit " + settings.SITE_URL + str(
                                    reverse("user_status", kwargs={"username": request.user.username})))

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


def export_attendance_xls(attendances):
    response = HttpResponse(content_type='applcation/ms/excel')
    response['Content-Disposition'] = 'attachment; filename="Attendance list.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Attendance')

    row_num = 0

    columns = ['Username', 'Check in','Check out','Duration']

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    for attendance in attendances:
        row_num += 1
        ws.write(row_num, 0, attendance.user.username, font_style)
        ws.write(row_num, 1, str(attendance.check_in.strftime("%Y-%m-%d - %a - %I:%M_%p")), font_style)
        ws.write(row_num, 2, str(attendance.check_out.strftime("%Y-%m-%d - %a - %I:%M_%p")), font_style)
        ws.write(row_num, 3, str(datetime.timedelta(milliseconds=attendance.duration)), font_style)

    wb.save(response)
    return response