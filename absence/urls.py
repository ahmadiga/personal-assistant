from django.conf.urls import url
from django_filters.views import FilterView
from absence import views
from absence.models import Leave

urlpatterns=[
    url(r'^leave-request/$', views.list_leave, name='leave_req'),
    url(r'^leave-new/$', views.new_leave, name='new_leave'),
    url(r'^leave-details/(\d+)$', views.leave_detail, name='leave_detail'),
    url(r'^leave-action/(\d+)/(\w+)$', views.leave_action, name='leave_action'),

]