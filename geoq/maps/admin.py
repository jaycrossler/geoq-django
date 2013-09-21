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
import reversion
from django.contrib.gis import admin
from models import Layer, Map, MapLayer, Feature, FeatureType


class MapLayerInline(admin.TabularInline):
    model = MapLayer
    extra = 1


class MapAdmin(reversion.VersionAdmin, admin.ModelAdmin):
    model = Map
    list_display = ['__unicode__', 'description']
    inlines = [MapLayerInline]
    save_as = True
    ordering = ['title']


class LayerAdmin(reversion.VersionAdmin, admin.OSMGeoAdmin):
    model = Layer
    list_display = ['name', 'type', 'image_format']
    list_filter = ['type', 'image_format']
    save_as = True
    search_fields = ['name']
    normal_fields = ('name', 'type', 'url', 'layer', 'attribution', 'description', 'image_format',
                     'styles', 'transparent', 'refreshrate')
    advanced_fields = ('enable_identify', 'token', 'additional_domains', 'constraints', 'extent',
                       'layer_parsing_function', 'info_format', 'root_field', 'fields_to_show',
                       'downloadableLink',  'spatial_reference', 'layer_params', )

    desc = 'The settings below are advanced.  Please contact and admin if you have questions.'
    fieldsets = (
        (None, {'fields': normal_fields}),
        ('Advanced Settings', {'classes': ('collapse',),
                               'description': desc,
                               'fields': advanced_fields,
                               }))


class MapLayerAdmin(reversion.VersionAdmin, admin.ModelAdmin):
    model = MapLayer
    list_display = ['__unicode__', 'map', 'layer', 'stack_order', 'opacity', 'is_base_layer']
    list_filter = ['map', 'layer', 'stack_order',  'is_base_layer']


class FeatureAdmin(reversion.VersionAdmin, admin.OSMGeoAdmin):
    list_display = ['template', 'aoi', 'project', 'analyst', 'created_at']


class FeatureTypeAdmin(reversion.VersionAdmin, admin.ModelAdmin):
    save_as = True

#admin.site.register(Point, FeatureAdmin)
#admin.site.register(Polygon, FeatureAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(FeatureType, FeatureTypeAdmin)
admin.site.register(Layer, LayerAdmin)
admin.site.register(Map, MapAdmin)
