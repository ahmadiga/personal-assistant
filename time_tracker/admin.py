from django.contrib import admin

# Register your models here.
from time_tracker.models import Client, Project, TimeEntry, Task

admin.site.register(Client)
admin.site.register(Project)
admin.site.register(TimeEntry)
admin.site.register(Task)
