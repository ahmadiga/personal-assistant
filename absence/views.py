from django.core.paginator import Paginator, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.urls import reverse
from django.utils import timezone

from absence.forms import LeaveForm, LeaveFilter
from absence.models import Leave
import xlwt


# leave_req view
from main.utils.slack import get_slack_user, post_message_on_channel
from django.conf import settings

def list_leave(request, id=None):
    if request.user.is_staff:
        leaves = Leave.objects.all().order_by('-submitted_date')
    else:
        leaves = Leave.objects.filter(user=request.user).order_by('-submitted_date')

    f = LeaveFilter(request.GET, queryset=leaves)
    if request.GET.get("excel", False):
        return export_leave_xls(f.qs)
    else:
        # Pagination
        page = request.GET.get('page', 1)
        paginator = Paginator(f.qs, 10)
        try:
            leaves = paginator.page(page)
        except PageNotAnInteger:
            leaves = paginator.page(1)
        return render(request, 'absence/leave_req.html', {'leaves': leaves, 'filter': f })


# leave_detail view
def leave_detail(request, id=None):
    leave = get_object_or_404(Leave, pk=id)
    return render(request, 'absence/leave_detail.html', {'leave': leave})


# form view
def new_leave(request):
    new_leave = Leave(user=request.user)
    form = LeaveForm(request.POST or None, instance=new_leave)
    if form.is_valid():
        form.save()
        post_message_on_channel("#absence",
                           get_slack_user(request.user) + " requested for a leave " + str(
                               timezone.localtime(timezone.now()).strftime(
                                   "%Y-%m-%d %H:%M")) + "\n for more info please visit" + settings.SITE_URL + str(
                               reverse("user_status", kwargs={"username": request.user.username})))
        return HttpResponse('success')

    return render(request, 'absence/new_leave.html', {'form': form})


# approving buttons
def leave_action(request, id, status):
    leave = get_object_or_404(Leave, pk=id)
    if status == "AP":
        leave.status = "AP"
        leave.approved_by = request.user
    elif status == "DA":
        leave.status = "DA"
        leave.approved_by = request.user
    leave.save()
    return redirect(reverse('leave_req'))


# Excel Sheet for list leave
def export_leave_xls(leaves):
    response = HttpResponse(content_type='application/ms/excel')
    response['Content-Disposition'] = 'attachment; filename="leave list.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Leave')

    row_num = 0

    columns = ['Username', 'Leave type', 'Submission Date', 'From date', 'To date']

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    for leave in leaves:
        row_num += 1
        ws.write(row_num, 0, leave.user.username, font_style)
        ws.write(row_num, 1, leave.get_type_display(), font_style)
        ws.write(row_num, 2, str(leave.submitted_date.strftime("%Y-%m-%d - %a - %I:%M_%p")), font_style)
        ws.write(row_num, 3, str(leave.pickFrom), font_style)
        ws.write(row_num, 4, str(leave.pickTo), font_style)

    wb.save(response)
    return response