from django import template
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from django.urls import reverse
from django.utils import timezone

from absence.models import Leave
from absence.forms import LeaveForm


def list_leave(request, id=None):
    if request.user.is_staff:
        leaves = Leave.objects.all().order_by('-submitted_date')
    else:
        leaves = Leave.objects.filter(user=request.user).order_by('-submitted_date')
    return render(request, 'absence/leave_req.html', {'leaves': leaves})


def leave_detail(request, id=None):
    leave = get_object_or_404(Leave, pk=id)
    return render(request, 'absence/leave_detail.html', {'leave': leave})


def new_leave(request):
    new_leave = Leave(user=request.user)
    form = LeaveForm(request.POST or None, instance=new_leave)
    if form.is_valid():
        form.save()
        return HttpResponse('success')

    return render(request, 'absence/new_leave.html', {'form': form})


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