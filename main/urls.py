from django.conf.urls import url
from main.forms import CustomRegistration, CustomLogin
from . import views
from registration.backends.simple import views as registration_views

urlpatterns = [
    url(r'^accounts/login/$', 'main.views.login',
        {'authentication_form': CustomLogin,}, name='registration_login'),
    url(r'^accounts/register/$', registration_views.RegistrationView.as_view(form_class=CustomRegistration),
        name='registration_register'),
    url(r'^$', views.index, name='home'),
]
