from django import forms
from django.forms.widgets import (RadioInput, RadioSelect, CheckboxInput,
    CheckboxSelectMultiple)
from models import AOI, Job, Project

no_style = [RadioInput, RadioSelect, CheckboxInput, CheckboxSelectMultiple]


class StyledModelForm(forms.ModelForm):
    """
    Adds the span5 (in reference to the Twitter Bootstrap element)
    to form fields.
    """
    cls = 'span5'

    def __init__(self, *args, **kwargs):
        super(StyledModelForm, self).__init__(*args, **kwargs)

        for f in self.fields:
            if type(self.fields[f].widget) not in no_style:
                self.fields[f].widget.attrs['class'] = self.cls


class AOIForm(StyledModelForm):
    class Meta:
        fields = ('name', 'description', 'job', 'analyst',
                  'priority', 'status')
        model = AOI


class JobForm(StyledModelForm):
    class Meta:

        fields = ('name', 'description', 'project',
                  'analysts', 'reviewers', "feature_types")
        model = Job


class ProjectForm(StyledModelForm):
    class Meta:
        fields = ('name', 'description', 'project_type', 'active', 'private')
        model = Project
