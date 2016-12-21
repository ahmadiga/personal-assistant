from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^list-client/$', views.list_client, name='list_client'),
    url(r'^manage-client/$', views.manage_client, name='manage_client'),
    url(r'^manage-client/(\d+)$', views.manage_client, name='manage_client'),
    url(r'^client-details/(\d+)$', views.client_details, name='client_details'),
    url(r'^list-project/$', views.list_project, name='list_project'),
    url(r'^manage-project/$', views.manage_project, name='manage_project'),
    url(r'^manage-project/(\d+)$', views.manage_project, name='manage_project'),
    url(r'^project-details/(\d+)$', views.project_details, name='project_details'),
    url(r'^list-timeentry/$', views.list_timeentry, name='list_timeentry'),
    url(r'^manage-timeentry/$', views.manage_timeentry, name='manage_timeentry'),
    url(r'^manage-timeentry/(\d+)$', views.manage_timeentry, name='manage_timeentry'),
    url(r'^timeentry-details/(\d+)$', views.timeentry_details, name='timeentry_details'),
    url(r'^end-entry/$', views.end_entry, name='end_entry'),
    url(r'^list-task/$', views.list_task, name='list_task'),
    url(r'^manage-task/(?P<username>\w+)/$', views.manage_task, name='manage_task'),
    url(r'^task-details/(\d+)$', views.task_details, name='task_details'),
    url(r'^create-task/(\d+)$', views.create_task, name='create_toggl_task'),
    url(r'^stop-task/(\d+)$', views.stop_task, name='stop_toggl_task'),
]
