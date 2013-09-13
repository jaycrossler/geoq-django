from core.forms import StyledModelForm
from django.forms.models import inlineformset_factory
from models import Feature, FeatureType, Map, Layer, MapLayer


class FeatureForm(StyledModelForm):
    class Meta:
        model = Feature
        exlcuded_fields = ("aoi")


class FeatureTypeForm(StyledModelForm):
    class Meta:
        model = FeatureType


class MapForm(StyledModelForm):
    class Meta:
        model = Map


class LayerForm(StyledModelForm):
    class Meta:
        model = Layer


class MapLayerForm(StyledModelForm):
    class Meta:
        model = MapLayer

MapInlineFormset = inlineformset_factory(Map, MapLayer)
