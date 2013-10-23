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
from django.core.urlresolvers import reverse_lazy
from django.utils.datastructures import SortedDict
import re


def menu(active=None, request_path=None):

    def order_dict(d, key):
        return SortedDict(sorted(d.items(), key=key))

    sort_key = lambda t:  t[1].get('index', None)

    help_dropdown = {
        'Submit Feedback':  {'index': 1, 'url':  reverse_lazy('home'), 'active': False},
        'FAQs':  {'index': 2, 'url': reverse_lazy('home'), 'active': False},
        }

    maps_dropdown = {
        'Maps':  {'index': 1, 'url': reverse_lazy('map-list'), 'active': False},
        'New Layer':  {'index': 2, 'url': reverse_lazy('layer-create'), 'active': False},
        'Feature Types':  {'index': 2, 'url': reverse_lazy('feature-type-list'), 'active': False}
    }

    menu_items = {
        'Projects': {'index': 2, 'url': reverse_lazy('project-list'), 'active': False},
        'Jobs': {'index': 3, 'url': reverse_lazy('job-list'), 'active': False},
        'Maps':  {'index': 4, 'url': '#', 'active': False, 'dropdown': order_dict(maps_dropdown, sort_key)},
        'Help': {'index': 6, 'url': '#', 'active': False, 'dropdown': order_dict(help_dropdown, sort_key)},
    }

    if request_path:
        for i in menu_items.keys():
            if menu_items[i].get('url', None):
                if re.search(str(menu_items[i].get('url')), request_path):
                    menu_items[i]['active'] = True

    return order_dict(menu_items, sort_key)
