import json
import requests
from core.models import AOI
from django.contrib.gis.geos import GEOSGeometry
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic import CreateView, DetailView, ListView, TemplateView, UpdateView, View
from forms import MapForm, MapInlineFormset
from models import Feature, FeatureType
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