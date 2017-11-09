from django.conf.urls import url

from absence import views

urlpatterns=[
    url(r'^leave-request/$', views.list_leave, name='leave_req'),
    url(r'^leave-new/$', views.new_leave, name='new_leave'),
    url(r'^leave-details/(\d+)$', views.leave_detail, name='leave_detail'),
    url(r'^leave-action/(\d+)/(\w+)$', views.leave_action, name='leave_action'),

]