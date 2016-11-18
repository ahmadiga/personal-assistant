from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from channels import Group
import json


# Create your views here.
@login_required
def index(request):
    Group("chat").send({
        "text": json.dumps({
            "text": "has entered the room",
            "user": request.user.username,
        })
    })

    return render(request, 'chat/index.html', {})
