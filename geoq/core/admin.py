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
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from models import Project, Job, AOI, UserProfile


class ObjectAdmin(admin.OSMGeoAdmin, reversion.VersionAdmin):
    list_display = ('name', 'created_at', 'updated_at')


class AOIAdmin(ObjectAdmin):
    filter_horizontal = ("reviewers",)
    save_on_top = True
    actions = ['rename_aois']

    class NameInputForm(forms.Form):
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        name_field = forms.CharField(max_length=200, required=True, label="AOI Name")

    def rename_aois(self, request, queryset):
        form = None

        if 'apply' in request.POST:
            form = self.NameInputForm(request.POST)

            if form.is_valid():
                namestring = form.cleaned_data['name_field']
                queryset.update( name=namestring )

                self.message_user(request, "Succesfully renamed selected AOIs")
                return HttpResponseRedirect(request.get_full_path())

        if not form:
            form = self.NameInputForm(initial={'_selected_action': request.POST.getlist('_selected_action')})

        return render(request, 'core/name_input.html', {'name_form': form})
    rename_aois.short_description = "Rename AOIs"


class JobAdmin(ObjectAdmin):
 	filter_horizontal = ("analysts","reviewers","feature_types")
 	save_on_top = True

class UserProfileAdmin(ObjectAdmin):
    list_display = ('user','score')

admin.site.register(Project, ObjectAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(AOI, AOIAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
