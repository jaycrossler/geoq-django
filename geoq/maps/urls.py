from django.conf.urls import patterns, url
from django.views.generic import CreateView, UpdateView
from forms import FeatureTypeForm, MapForm, LayerForm, MapLayerForm
from views import CreateFeatures, CreateMapView

urlpatterns = patterns('',

    url(r'^features/create/?$',
        CreateFeatures.as_view(),
        name='feature-create'),

    url(r'^feature-types/create/?',
        CreateView.as_view(template_name='core/generic_form.html',
                           form_class=FeatureTypeForm),
        name='feature-type-create'),

    url(r'^feature-types/update/(?P<pk>\d+)/?$',
        UpdateView.as_view(template_name='core/generic_form.html',
                           queryset=FeatureTypeForm.Meta.model.objects.all(),
                           form_class=FeatureTypeForm),
        name='feature-type-update'),

    # Map CRUD Views
    url(r'^create/?$',
        CreateMapView.as_view(template_name='core/generic_form.html', form_class=MapForm),
        name='map-create'),

    url(r'^update/(?P<pk>\d+)/?$',
        UpdateView.as_view(template_name='core/generic_form.html',
                           queryset=MapForm.Meta.model.objects.all(),
                           form_class=MapForm),
        name='map-update'),

    # Layer CRUD Views
    url(r'^layers/create/?$',
        CreateView.as_view(template_name='core/generic_form.html', form_class=LayerForm),
        name='layer-create'),

    url(r'^layers/update/(?P<pk>\d+)/?$',
        UpdateView.as_view(template_name='core/generic_form.html',
                           queryset=LayerForm.Meta.model.objects.all(),
                           form_class=LayerForm),
        name='layer-update'),

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
