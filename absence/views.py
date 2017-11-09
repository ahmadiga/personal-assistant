from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

from absence.models import Leave
from absence.forms import LeaveForm


def list_leave(request, id=None):
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

    return render(request,'absence/new_leave.html',{'form': form })


def leave_action(request, id,status):
    leave = get_object_or_404(Leave, pk=id)
    if status == "AP":
        leave.status = "AP"
    elif status == "DA":
        leave.status = "DA"
    leave.save()
    return redirect(reverse('leave_req'))