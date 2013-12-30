# -*- coding: utf-8 -*-
from django.test import Client
from django.test import TestCase


class MapsTest(TestCase):

    def test_create_features_view(self):
        """
        Tests the CreateFeatures View.

        Given an AOI id and geometry and properties as GeoJSON create a new feature.  Error should return a
        human readable message with numeric response status both as JSON.
        """

        pass

    def test_create_map_view(self):
        """
        Tests the CreateMap view.

        View renders both the Map form and an inline form for map layers.

        Context data returned:
        form: The Map ModelForm.
        custom_form: The inline map layer form.
        """

        pass
