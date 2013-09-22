# -*- coding: utf-8 -*-

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, as long as
# any reuse or further development of the software attributes the
# National Geospatial-Intelligence Agency (NGA) auhtorship as follows:
# 'This software (GeoQ or Geographic Work Queueing and Tasking System)
# is provided to the public as a courtesy of the National
# Geospatial-Intelligence Agency.
#  
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#  
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from django.conf.urls import patterns, url
from django.views.generic import CreateView, TemplateView, ListView, UpdateView
from forms import AOIForm, JobForm, ProjectForm
from models import AOI, Project, Job
from views import BatchCreateAOIS, CreateFeaturesView, Dashboard, DetailedListView, JobDetailedListView, ChangeAOIStatus,\
    JobDelete, AOIDelete, CreateJobView, redirect_to_unassigned_aoi

urlpatterns = patterns('',
    url(r'^$', Dashboard.as_view(), name='home'),

    # PROJECTS
    url(r'^projects/?$',
        ListView.as_view(queryset=Project.objects.all()),
                         name='project-list'),

    url(r'^projects/(?P<pk>\d+)/?$',
        DetailedListView.as_view(template_name="core/project_detail.html"),
        name='project-detail'),

    url(r'^projects/create/?$',
        CreateView.as_view(form_class=ProjectForm,
                           template_name="core/generic_form.html"),
                           name='project-create'),
    url(r'^projects/update/(?P<pk>\d+)/?$',
        UpdateView.as_view(queryset=Project.objects.all(),
                           template_name='core/generic_form.html',
                           form_class=ProjectForm),
        name='project-update'),

    # JOBS
    url(r'^jobs/?$', ListView.as_view(queryset=Job.objects.all()), name='job-list'),
    url(r'^jobs/(?P<pk>\d+)/(?P<status>[a-zA-Z_ ]+)?/?$',
        JobDetailedListView.as_view(template_name='core/job_detail.html'),
        name='job-detail'),
    url(r'^jobs/(?P<pk>\d+)/next-aoi', redirect_to_unassigned_aoi, name='job-next-aoi'),
    url(r'^jobs/create/?$',
        CreateJobView.as_view(queryset=Job.objects.all(),
                           template_name='core/generic_form.html',
                           form_class=JobForm),
        name='job-create'),
    url(r'^jobs/update/(?P<pk>\d+)/?$',
        UpdateView.as_view(queryset=Job.objects.all(),
                           template_name='core/generic_form.html',
                           form_class=JobForm),
        name='job-update'),
    url(r'^jobs/delete/(?P<pk>\d+)/?$',
        JobDelete.as_view(),
        name='job-delete'),
    url(r'^jobs/(?P<job_pk>\d+)/batch-create-aois/?$',
        BatchCreateAOIS.as_view(),
        name='job-batch-create-aois'),

    # AOIS
    url(r'^aois/work/(?P<pk>\d+)/?$', CreateFeaturesView.as_view(), name='aoi-work'),
    url(r'^aois/update-status/(?P<pk>\d+)/(?P<status>Unassigned|Assigned|In work|Submitted|Completed)/?$',
        ChangeAOIStatus.as_view(), name="aoi-update-status"),
    url(r'^aois/create/?$',
        CreateView.as_view(queryset=AOI.objects.all(),
                           template_name='core/generic_form.html',
                           form_class=AOIForm),
        name='aoi-create'),
    url(r'^aois/update/(?P<pk>\d+)/?$',
        UpdateView.as_view(queryset=AOI.objects.all(),
                           template_name='core/generic_form.html',
                           form_class=AOIForm),
        name='aoi-update'),
    url(r'^aois/delete/(?P<pk>\d+)/?$',
        AOIDelete.as_view(),
        name='aoi-delete'),

    # OTHER URLS
    url(r'^edit/?$', TemplateView.as_view(template_name='core/edit.html'), name='edit'),
    url(r'^api/geo/usng/?$', 'core.views.usng', name='usng'),

)
