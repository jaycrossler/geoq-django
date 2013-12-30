# -*- coding: utf-8 -*-
from django import template
register = template.Library()

@register.filter('object_class')
def field_class(ob):
    """
    Returns the class of the object
    """
    return ob.__class__.__name__
