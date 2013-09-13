import json
import requests
from core.models import AOI
from django.contrib.gis.geos import GEOSGeometry
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, ListView, TemplateView, UpdateView, View
from django.views.generic.edit import BaseCreateView
from forms import MapInlineFormset
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


class CreateMapView(CreateView):
    """
    Renders both the Map form and an inline form for map layers.
    """

    def get_context_data(self, **kwargs):
        cv = super(CreateMapView, self).get_context_data(**kwargs)
        #TODO: Multiple form processing is currently not working.
        cv['map_layers'] = MapInlineFormset()
        cv['custom_form'] = "maps/_maps_form.html"
        return cv
