from django.contrib import admin

# Register your models here.
from attendance.models import Attendance

admin.site.register(Attendance)
