# forms.py
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Submit
from crispy_forms.layout import Layout
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.forms import AuthenticationForm
from parsley.decorators import parsleyfy
from registration.forms import RegistrationFormUniqueEmail
from django.forms import ModelForm, forms, CharField, EmailField
from django.conf import settings

from main.models import Profile


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


@parsleyfy
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {"data-parsley-validate": "data-parsley-validate"}
        self.helper.layout = Layout(
            Div(
                Div('slack_token', css_class="col-md-6"),
                Div('toggl_token', css_class="col-md-6"),
                css_class="row"),
            Div(
                Div(Div(Submit('save', _('Save Changes'), css_class='btn btn-success btn-block'),
                        css_class="col-md-6 col-md-offset-3"),
                    css_class="row")
            )
        )

# @parsleyfy
# class ProfileForm(ModelForm):
#    class Meta:
#        model = Profile
#        exclude = []
#    def __init__(self, *args, **kwargs):
#        super(ProfileForm, self).__init__(*args, **kwargs)
#        self.helper = FormHelper()
#        self.helper.attrs = {"data-parsley-validate": "data-parsley-validate"}
#        self.helper.layout = Layout(
#            Div(
#                    Div('slack_token', css_class="col-md-6"),
#                    Div('toggl_token', css_class="col-md-6"),
#                css_class="row"),
#                Div(
#                    Div('user', css_class="col-md-6"),
#            Div(Div(Submit('save', _('Save Changes'), css_class='btn btn-success btn-block'),css_class="col-md-6 col-md-offset-3"),
#               css_class="row")
#        )
#    )
