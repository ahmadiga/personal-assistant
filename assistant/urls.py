from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^list-task/$', views.list_task, name='list_task'),
    url(r'^manage-task/(?P<username>\w+)/$', views.manage_task, name='manage_task'),
    url(r'^task-details/(\d+)$', views.task_details, name='task_details'),
    url(r'^create_toggl-task/(\d+)$', views.create_toggl_task, name='create_toggl_task'),
    url(r'^stop-toggl-task/(\d+)$', views.stop_toggl_task, name='stop_toggl_task'),
    url(r'^list-project/$', views.list_project, name='list_project'),
    url(r'^manage-project/(\d+)$', views.manage_project, name='manage_project'),
]
