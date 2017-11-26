import django_filters
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit
from django.forms import ModelForm
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from parsley.decorators import parsleyfy

from attendance.models import Attendance


class AttendanceFilter(django_filters.FilterSet):

    class Meta:
        model = Attendance
        fields = ['user']


@parsleyfy
class AttendanceForm(ModelForm):
    class Meta:
        model = Attendance
        exclude = ['user', 'duration']

    def __init__(self, *args, **kwargs):
        super(AttendanceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = reverse("manage_attendance", args=(self.instance.id,))
        self.helper.attrs = {"data-parsley-validate": "data-parsley-validate"}
        self.helper.layout = Layout(
            Div(
                Div('check_in', css_class="col-md-6"),
                Div('check_out', css_class="col-md-6"),
                css_class="row"),
            Div(
                Div(Div(Submit('save', _('Save Changes'), css_class='btn btn-success btn-block'),
                        css_class="col-md-6 col-md-offset-3"),
                    css_class="row")
            )
        )
