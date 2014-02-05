# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.views.generic import CreateView, UpdateView, ListView
from forms import FeatureTypeForm, MapForm, LayerForm, MapLayerForm
from views import CreateFeatures, create_map, FeatureTypeListView, FeatureTypeDelete, MapListView, MapDelete, LayerListView, LayerDelete, LayerImport
from models import FeatureType, Map, Layer

urlpatterns = patterns('',

    url(r'^features/create/?$',
        CreateFeatures.as_view(),
        name='feature-create'),

    url(r'^feature-types/?$',
        FeatureTypeListView.as_view(queryset=FeatureType.objects.all()),
                         name='feature-type-list'),

    url(r'^feature-types/create/?',
        CreateView.as_view(template_name='core/generic_form.html',
                           form_class=FeatureTypeForm),
        name='feature-type-create'),

    url(r'^feature-types/update/(?P<pk>\d+)/?$',
        UpdateView.as_view(template_name='core/generic_form.html',
                           queryset=FeatureTypeForm.Meta.model.objects.all(),
                           form_class=FeatureTypeForm),
        name='feature-type-update'),

    url(r'^feature-types/delete/(?P<pk>\d+)/?$',
        FeatureTypeDelete.as_view(),
        name='feature-type-delete'),

    # Map list
    url(r'^maps/?$', MapListView.as_view(queryset=Map.objects.all()),
                                              name='map-list'),

    url(r'^maps/delete/(?P<pk>\d+)/?$',
        MapDelete.as_view(),
        name='map-delete'),


    # Map CRUD Views
    url(r'^create/?$',
        create_map,
        name='map-create'),

    url(r'^update/(?P<pk>\d+)/?$',
        UpdateView.as_view(template_name='core/generic_form.html',
                           queryset=MapForm.Meta.model.objects.all(),
                           form_class=MapForm),
        name='map-update'),

    # Layer CRUD Views
    url(r'^layers/?$',
        LayerListView.as_view(queryset=Layer.objects.all()),
                         name='layer-list'),

    url(r'^layers/create/?$',
        CreateView.as_view(template_name='core/generic_form.html', form_class=LayerForm),
        name='layer-create'),

    url(r'^layers/update/(?P<pk>\d+)/?$',
        UpdateView.as_view(template_name='core/generic_form.html',
                           queryset=LayerForm.Meta.model.objects.all(),
                           form_class=LayerForm),
        name='layer-update'),

    url(r'^layers/delete/(?P<pk>\d+)/?$',
        LayerDelete.as_view(),
        name='layer-delete'),

    url(r'^layers/import/?$',
        LayerImport.as_view(),
        name='layer-import'),

    # MapLayer CRUD Views
    url(r'^map-layers/create/?$',
        CreateView.as_view(template_name='core/generic_form.html',
                           form_class=MapLayerForm),
        name='map-layer-create'),

    url(r'^map-layers/update/(?P<pk>\d+)/?$',
        UpdateView.as_view(template_name='core/generic_form.html',
                           queryset=MapLayerForm.Meta.model.objects.all(),
                           form_class=MapLayerForm),
        name='map-layer-update'),
)
