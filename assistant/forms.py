from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Submit
from crispy_forms.layout import Layout
from django.forms import ModelForm
from parsley.decorators import parsleyfy
from django.utils.translation import ugettext_lazy as _

from assistant.models import Task, Project


@parsleyfy
class TaskForm(ModelForm):
    class Meta:
        model = Task
        exclude = ["submitted_for", "submitted_by", "estimated_time", "create_date", "status", "time_entry_id"]

    def __init__(self, *args, **kwargs):
        user = kwargs["user"]
        kwargs.pop("user")
        super(TaskForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {"data-parsley-validate": "data-parsley-validate"}
        self.fields["project"].queryset = Project.objects.filter(user=user)
        self.helper.layout = Layout(
            Div(
                Div('title', css_class="col-md-12"),
                css_class="row"),
            Div(
                Div('description', css_class="col-md-12"),
                css_class="row"),
            Div(
                Div('priority', css_class="col-md-6"),
                Div('project', css_class="col-md-6"),
                css_class="row"),
            Div(
                Div(Div(Submit('save', _('Save Changes'), css_class='btn btn-success btn-block'),
                        css_class="col-md-6 col-md-offset-3"),
                    css_class="row")
            )
        )


@parsleyfy
class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ["name", "toggl_id", "client", "user", "", "", ]

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {"data-parsley-validate": "data-parsley-validate"}
        self.helper.layout = Layout(

            Div(
                Div('slack_channel', css_class="col-md-12"),
                css_class="row"),
            Div(
                Div(Div(Submit('save', _('Save Changes'), css_class='btn btn-success btn-block'),
                        css_class="col-md-6 col-md-offset-3"),
                    css_class="row")
            )
        )
