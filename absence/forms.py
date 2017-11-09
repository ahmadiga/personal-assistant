from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Fieldset, Field
from django import forms
from django.urls import reverse
from parsley.decorators import parsleyfy

from absence.models import Leave


@parsleyfy
class LeaveForm(forms.ModelForm):

    class Meta:
        model = Leave
        fields = ('type', 'pickFrom', 'pickTo', 'description')

    def __init__(self, *args, **kwargs):
        super(LeaveForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {"data-parsley-validate": "data-parsley-validate"}
        self.helper.form_action = reverse("new_leave")
        self.helper.layout = Layout(
            Div(
                Div('type', css_class="col-md-12"),
                css_class="row"),
            Div(
                Div('pickFrom', css_class="col-md-6"),
                Div('pickTo', css_class="col-md-6"),
                css_class="row"),
            Div(
                Div('description', css_class="col-md-12"),
                css_class="row"),
            Div(
                Div(
                    Submit('save', 'Save Changes', css_class='btn btn-success btn-block'),
                    css_class="col-md-6 col-md-offset-3"),
                css_class="row"),
        )
