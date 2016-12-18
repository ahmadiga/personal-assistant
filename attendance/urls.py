from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.list_attendance, name='list_attendance'),
    url(r'^manage-attendance/$', views.manage_attendance, name='manage_attendance'),
    url(r'^manage-attendance/(\d+)$', views.manage_attendance, name='manage_attendance'),
    url(r'^attendance-details/(\d+)$', views.attendance_details, name='attendance_details'),
    url(r'^checkin/$', views.checkin, name='attendance_checkin'),
    url(r'^checkout/$', views.checkout, name='attendance_checkout'),
]
