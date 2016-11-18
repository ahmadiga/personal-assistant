# forms.py
from django.contrib.auth.forms import AuthenticationForm
from registration.forms import RegistrationFormUniqueEmail
from django.forms import ModelForm, forms, CharField, EmailField
from django.conf import settings


class CustomRegistration(RegistrationFormUniqueEmail):
    pass


class CustomLogin(AuthenticationForm):
    if settings.DSK_LOGIN_FIELDS == "email_username":
        username = CharField(max_length=254, label="Username or Email")
    elif settings.DSK_LOGIN_FIELDS == "username":
        username = CharField(max_length=254, label="Username")
    elif settings.DSK_LOGIN_FIELDS == "email":
        username = EmailField(max_length=254, label="Email")
    pass
