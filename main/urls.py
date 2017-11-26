from django.conf.urls import url, include
from main.forms import CustomRegistration, CustomLogin
from . import views
from registration.backends.simple import views as registration_views

urlpatterns = [
    url(r'^accounts/login/$', views.login,
        {'authentication_form': CustomLogin,}, name='registration_login'),
    url(r'^accounts/register/$', registration_views.RegistrationView.as_view(form_class=CustomRegistration),
        name='registration_register'),
    url(r'^$', views.index, name='home'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^status/(?P<username>[-\w.]+)/$', views.dashboard, name='user_status'),
    url(r'^attendance/', include('attendance.urls')),
    url(r'^absence/', include('absence.urls')),
    url(r'^performance/', include('performance.urls')),
    url(r'^time-tracker/', include('time_tracker.urls')),
    url(r'^manage-profile$', views.manage_profile, name='manage_profile'),
    url(r'^profile-details/(\d+)$', views.profile_details, name='profile_details'),
    url(r'^list-profile/$', views.list_profile, name='list_profile'),
    url(r'^update-projects/$', views.update_projects, name='update_projects'),
    url(r'^report_builder/', include('report_builder.urls'))
]
