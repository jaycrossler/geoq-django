# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.views.generic import CreateView, TemplateView, ListView, UpdateView
from forms import AOIForm, JobForm, ProjectForm
from models import AOI, Project, Job
from views import (BatchCreateAOIS, CreateFeaturesView, Dashboard, DetailedListView,
    JobDetailedListView, ChangeAOIStatus, JobDelete, AOIDelete, CreateJobView,
    CreateProjectView, redirect_to_unassigned_aoi)

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
        CreateProjectView.as_view(form_class=ProjectForm,
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
    url(r'^jobs/(?P<job_pk>\d+)/create-aois/?$',
        BatchCreateAOIS.as_view(),
        name='job-create-aois'),
    url(r'^jobs/(?P<job_pk>\d+)/batch-create-aois/?$',
        'core.views.batch_create_aois', name='job-batch-create-aois'),

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
