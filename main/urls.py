from django.conf.urls import url, include
from main.forms import CustomRegistration, CustomLogin
from . import views
from registration.backends.simple import views as registration_views

urlpatterns = [
    url(r'^accounts/login/$', 'main.views.login',
        {'authentication_form': CustomLogin,}, name='registration_login'),
    url(r'^accounts/register/$', registration_views.RegistrationView.as_view(form_class=CustomRegistration),
        name='registration_register'),
    url(r'^$', views.index, name='home'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^status/(?P<username>\w+)/$', views.dashboard, name='user_status'),
    url(r'^assistant/', include('assistant.urls')),
    url(r'^manage-profile$', views.manage_profile, name='manage_profile'),
    url(r'^profile-details/(\d+)$', views.profile_details, name='profile_details'),
    url(r'^list-profile/$', views.list_profile, name='list_profile'),
    url(r'^update-projects/$', views.update_projects, name='update_projects'),

]
