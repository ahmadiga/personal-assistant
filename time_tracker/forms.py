from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from parsley.decorators import parsleyfy

from django.utils.translation import ugettext_lazy as _

from time_tracker.models import Client, Project, TimeEntry, Task


@parsleyfy
class ClientForm(ModelForm):
    class Meta:
        model = Client
        exclude = []

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {"data-parsley-validate": "data-parsley-validate"}
        self.helper.layout = Layout(
            Div(
                Div('name', css_class="col-md-6"),
                Div(Div(Submit('save', _('Save Changes'), css_class='btn btn-success btn-block'),
                        css_class="col-md-6 col-md-offset-3"),
                    css_class="row")
            )
        )


@parsleyfy
class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = []

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {"data-parsley-validate": "data-parsley-validate"}
        self.helper.layout = Layout(
            Div(
                Div('name', css_class="col-md-6"),
                Div('client', css_class="col-md-6"),
                css_class="row"),
            Div(
                Div(Div(Submit('save', _('Save Changes'), css_class='btn btn-success btn-block'),
                        css_class="col-md-6 col-md-offset-3"),
                    css_class="row")
            )
        )


@parsleyfy
class TimeEntryForm(ModelForm):
    class Meta:
        model = TimeEntry
        exclude = ["started_at", "ended_at", "duration", "task", "user"]

    def __init__(self, *args, **kwargs):
        super(TimeEntryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {"data-parsley-validate": "data-parsley-validate"}
        self.helper.form_action = reverse("manage_timeentry")
        self.helper.layout = Layout(
            Div(
                Div('title', css_class="col-md-12"),
                css_class="row"),
            Div(
                Div('description', css_class="col-md-12"),
                css_class="row"),
            Div(
                Div('project', css_class="col-md-12"),
                css_class="row"),
            Div(
                Div(Submit('save', _('Save Changes'), css_class='btn btn-success btn-block'),
                    css_class="col-md-12"),
                css_class="row"),
        )


@parsleyfy
class UpdateTimeEntryForm(ModelForm):
    class Meta:
        model = TimeEntry
        exclude = ["duration", "task", "user"]

    def __init__(self, *args, **kwargs):
        super(UpdateTimeEntryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {"data-parsley-validate": "data-parsley-validate"}
        self.helper.form_action = reverse("manage_timeentry", args=(self.instance.id,))
        self.helper.layout = Layout(
            Div(
                Div('title', css_class="col-md-12"),
                css_class="row"),
            Div(
                Div('description', css_class="col-md-12"),
                css_class="row"),
            Div(
                Div('project', css_class="col-md-12"),
                css_class="row"),
            Div(
                Div('started_at', css_class="col-md-12"),
                css_class="row"),
            Div(
                Div('ended_at', css_class="col-md-12"),
                css_class="row"),
            Div(
                Div(Submit('save', _('Save Changes'), css_class='btn btn-success btn-block'),
                    css_class="col-md-12"),
                css_class="row"),
        )


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
        self.helper.form_action = reverse("manage_task", kwargs={"username": user.username})
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
