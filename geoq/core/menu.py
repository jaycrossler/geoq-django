# -*- coding: utf-8 -*-
# This technical data was produced for the U. S. Government under Contract No. W15P7T-13-C-F600, and
# is subject to the Rights in Technical Data-Noncommercial Items clause at DFARS 252.227-7013 (FEB 2012)

from django.core.urlresolvers import reverse_lazy
from django.utils.datastructures import SortedDict
import re


def menu(active=None, request_path=None):

    def order_dict(d, key):
        return SortedDict(sorted(d.items(), key=key))

    sort_key = lambda t:  t[1].get('index', None)

    #help_dropdown = {
    #    'Submit Feedback':  {'index': 1, 'url':  reverse_lazy('home'), 'active': False},
    #    'FAQs':  {'index': 2, 'url': reverse_lazy('home'), 'active': False},
    #    }

    maps_dropdown = {
        'Maps':  {'index': 1, 'url': reverse_lazy('map-list'), 'active': False},
        'Layers':  {'index': 2, 'url': reverse_lazy('layer-list'), 'active': False},
        'Feature Types':  {'index': 2, 'url': reverse_lazy('feature-type-list'), 'active': False}
    }

    menu_items = {
        'Projects': {'index': 2, 'url': reverse_lazy('project-list'), 'active': False},
        'Jobs': {'index': 3, 'url': reverse_lazy('job-list'), 'active': False},
        'Maps':  {'index': 4, 'url': '#', 'active': False, 'dropdown': order_dict(maps_dropdown, sort_key)},
        # 'Help': {'index': 6, 'url': '#', 'active': False, 'dropdown': order_dict(help_dropdown, sort_key)},
    }

    if request_path:
        for i in menu_items.keys():
            if menu_items[i].get('url', None):
                if re.search(str(menu_items[i].get('url')), request_path):
                    menu_items[i]['active'] = True

    return order_dict(menu_items, sort_key)
