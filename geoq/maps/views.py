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
from core.models import AOI
from django.contrib.gis.geos import GEOSGeometry
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic import CreateView, DetailView, ListView, TemplateView, UpdateView, View, DeleteView
from forms import MapForm, MapInlineFormset
from models import Feature, FeatureType, Map
import logging

logger = logging.getLogger(__name__)


class CreateFeatures(View):
    """
    Reads GeoJSON from post request and creates AOIS for each features.
    """

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        feature = None
        aoi = request.POST.get('aoi')
        geometry = request.POST.get('geometry')
        geojson = json.loads(geometry)
        properties = geojson.get('properties')

        aoi = AOI.objects.get(id=aoi)
        job = getattr(aoi, 'job')
        project = getattr(job, 'project')
        template = properties.get('template') if properties else None

        #TODO: handle exceptions
        if template:
            template = FeatureType.objects.get(id=template)

        attrs = dict(aoi=aoi,
                     job=job,
                     project=project,
                     analyst=request.user,
                     template=template)

        geometry = geojson.get('geometry')
        attrs['the_geom'] = GEOSGeometry(json.dumps(geometry))

        try:
            response = Feature(**attrs)
            response.full_clean()
            response.save()
        except ValidationError as e:
            return HttpResponse(content=json.dumps(dict(errors=e.messages)), mimetype="application/json", status=400)

        return HttpResponse([response], mimetype="application/json")


def create_map(request):

    if request.method == 'POST':
        map = MapForm(request.POST, prefix='map')
        layer_formset = MapInlineFormset(request.POST, prefix='layers')
        if map.is_valid() and layer_formset.is_valid():
            # do something with the cleaned_data on the formsets.
            m = map.save(commit=False)
            layer_formset.instance = m
            m.save()
            layer_formset.save()
            return HttpResponseRedirect(reverse('job-list'))
    else:
        map = MapForm(prefix='map')
        layer_formset = MapInlineFormset(prefix='layers')
        print layer_formset.management_form.as_p
    return render_to_response('core/generic_form.html', {
        'form': map,
        'layer_formset': layer_formset,
        'custom_form': 'core/map_create.html',
        },context_instance=RequestContext(request))

class MapListView(ListView):
    model = Map

    def get_context_data(self,**kwargs):
        context = super(MapListView, self).get_context_data(**kwargs)
        return context

class MapDelete(DeleteView):
    model = Map
    template_name = "core/generic_confirm_delete.html"

    def get_success_url(self):
        return reverse('map-list')


class FeatureTypeListView(ListView):

    model = FeatureType

    def get_context_data(self,**kwargs):
        context = super(FeatureTypeListView, self).get_context_data(**kwargs)
        return context


class FeatureTypeDelete(DeleteView):
    model = FeatureType
    template_name = "core/generic_confirm_delete.html"

    def get_success_url(self):
        return reverse('feature-type-update')