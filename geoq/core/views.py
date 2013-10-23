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
import json
import requests

from django.contrib.auth.models import User
from django.contrib.gis.geos import GEOSGeometry
from django.forms.util import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, TemplateView, View, DeleteView, CreateView
from django.core.urlresolvers import reverse

from teamwork.models import Team

from models import Project, Job, AOI
from maps.models import Layer, Map


class Dashboard(TemplateView):

    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        cv = super(Dashboard, self).get_context_data(**kwargs)
        cv['projects'] = Project.objects.all()
        return cv


class BatchCreateAOIS(TemplateView):
    """
    Reads GeoJSON from post request and creates AOIS for each features.
    """
    template_name = 'core/job_batch_create_aois.html'

    def get_context_data(self, **kwargs):
        cv = super(BatchCreateAOIS, self).get_context_data(**kwargs)
        cv['object'] = get_object_or_404(Job, pk=self.kwargs.get('job_pk'))
        return cv

    def post(self, request, *args, **kwargs):
        aois = request.POST.get('aois')
        job = Job.objects.get(id=self.kwargs.get('job_pk'))

        try:
            aois = json.loads(aois)
        except ValueError:
            raise ValidationError(_("Enter valid JSON"))

        response = AOI.objects.bulk_create([AOI(name=job.name,
                                            job=job,
                                            description=job.description,
                                            polygon=GEOSGeometry(json.dumps(aoi.get('geometry')))) for aoi in aois])

        return HttpResponse([aoi.geoJSON() for aoi in response], mimetype="application/json")


#TODO: Abstract this
class DetailedListView(ListView):
    """
    A mixture between a list view and detailed view.
    """

    paginate_by = 15
    model = Project

    def get_queryset(self):
        return Job.objects.filter(project=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        cv = super(DetailedListView, self).get_context_data(**kwargs)
        cv['object'] = get_object_or_404(self.model, pk=self.kwargs.get('pk'))
        return cv


class CreateFeaturesView(DetailView):
    template_name = 'core/edit.html'
    queryset = AOI.objects.all()

    def get_context_data(self, **kwargs):
        cv = super(CreateFeaturesView, self).get_context_data(**kwargs)
        cv['map'] = self.object.job.map
        return cv


def redirect_to_unassigned_aoi(request, pk):
    """
    Given a job, redirects the view to an unassigned AOI.  If there are no unassigned AOIs, the user will be redirected
     to the job's absolute url.
    """
    job = get_object_or_404(Job, id=pk)

    try:
        return HttpResponseRedirect(job.aois.filter(status='Unassigned')[0].get_absolute_url())
    except IndexError:
        return HttpResponseRedirect(job.get_absolute_url())



class JobDetailedListView(ListView):
    """
    A mixture between a list view and detailed view.
    """

    paginate_by = 15
    model = Job
    default_status = 'unassigned'

    def get_queryset(self):
        status = getattr(self, 'status', None)
        self.queryset = AOI.objects.filter(job=self.kwargs.get('pk'))
        if status and (status in [value.lower() for value in AOI.STATUS_VALUES]):
            return self.queryset.filter(status__iexact=status)
        else:
            return self.queryset

    def get(self, request, *args, **kwargs):
        self.status = self.kwargs.get('status')

        if self.status and hasattr(self.status, "lower"):
            self.status = self.status.lower()
        else:
            self.status = self.default_status.lower()

        return super(JobDetailedListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        cv = super(JobDetailedListView, self).get_context_data(**kwargs)
        cv['object'] = get_object_or_404(self.model, pk=self.kwargs.get('pk'))
        cv['statuses'] = AOI.STATUS_VALUES
        cv['active_status'] = self.status
        return cv


class JobDelete(DeleteView):
    model = Job
    template_name = "core/generic_confirm_delete.html"

    def get_success_url(self):
        return reverse('project-detail', args=[self.object.project.pk])


class AOIDelete(DeleteView):
    model = AOI
    template_name = "core/generic_confirm_delete.html"

    def get_success_url(self):
        return reverse('job-detail', args=[self.object.job.pk])

class CreateProjectView(CreateView):
    """
    Create view that adds the user that created the job as a reviewer.
    """

    def form_valid(self, form):
        """
        If the form is valid, save the associated model and add the current user as a reviewer.
        """
        self.object = form.save()
        self.object.supervisors.add(self.request.user)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class CreateJobView(CreateView):
    """
    Create view that adds the user that created the job as a reviewer.
    """

    def form_valid(self, form):
        """
        If the form is valid, save the associated model and add the current user as a reviewer.
        """
        self.object = form.save()
        self.object.reviewers.add(self.request.user)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ChangeAOIStatus(View):
    http_method_names = ['post']

    def post(self, request, **kwargs):
        aoi = get_object_or_404(AOI, pk=self.kwargs.get('pk'))
        status = self.kwargs.get('status')

        if aoi.user_can_complete(request.user):
            aoi.status = status
            aoi.save()
            return HttpResponse(json.dumps({aoi.id: aoi.status}), mimetype="application/json")
        else:
            error = dict(error=403,
                         details="User not allowed to modify the status of this AOI.",)
            return HttpResponse(json.dumps(error), status=error.get('error'))


def usng(request):
    """
    Proxy to USNG service.
    """

    base_url = "http://app01.ozone.nga.mil/geoserver/wfs"

    bbox = request.GET.get('bbox')

    if not bbox:
        return HttpResponse()

    params = dict()
    params['service'] = 'wfs'
    params['version'] = '1.0.0'
    params['request'] = 'GetFeature'
    params['typeName'] = 'usng'
    params['bbox'] = bbox
    params['outputFormat'] = 'json'
    params['srsName'] = 'EPSG:4326'
    resp = requests.get(base_url, params=params)
    return HttpResponse(resp, mimetype="application/json")
